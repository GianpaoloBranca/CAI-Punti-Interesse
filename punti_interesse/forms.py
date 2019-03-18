from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from punti_interesse.models import PuntoInteresse, FotoAccessoria, ValidazionePunto, InteresseSpecifico
from countable_field.widgets import CountableWidget

class PuntoInteresseForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    latitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)
    longitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sottocategoria'].queryset = InteresseSpecifico.objects.none()

        # called when data submitted in POST
        if 'categoria' in self.data:
            try:
                categoria = int(self.data.get('categoria'))
                self.fields['sottocategoria'].queryset = InteresseSpecifico.objects.filter(tipo=categoria)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.id:
            categoria = self.instance.categoria.id
            self.fields['sottocategoria'].queryset = InteresseSpecifico.objects.filter(tipo=categoria)

    class Meta:
        model = PuntoInteresse
        fields = (
            'nome',
            'categoria',
            'sottocategoria',
            'longitudine',
            'latitudine',
            'localita',
            'valle',
            'qualita',
            'estensione',
            'stato_conservazione',
            'valenza',
            'visitabile',
            'visitabile2',
            'periodo',
            'istituto',
            'descr_breve',
            'descr_estesa',
            'descr_sito',
            'motivo',
            'rif_biblio',
            'rif_sito',
            'foto_copertina',
        )
        widgets = {
            'descr_estesa'  : CountableWidget(attrs={'rows':8, 'cols':40}),
            'descr_breve'   : CountableWidget(attrs={'rows':4, 'cols':40}),
            'descr_sito'    : CountableWidget(attrs={'rows':4, 'cols':40}),
            'motivo'        : CountableWidget(attrs={'rows':2, 'cols':40}),
            'rif_biblio'    : CountableWidget(attrs={'rows':2, 'cols':40}),
            'rif_sito'      : CountableWidget(attrs={'rows':2, 'cols':40})
        }


class FotoAccessoriaForm(forms.ModelForm):

    class Meta:
        model = FotoAccessoria
        fields = ('foto',)


class ValidazioneForm(forms.ModelForm):
    quota = forms.IntegerField(min_value=0)

    class Meta:
        model = ValidazionePunto
        fields = (
            'regione',
            'comunita_montana',
            'gruppo_montuoso',
            'quota',
            'descrizione',
        )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password',)
