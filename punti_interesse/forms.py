from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from punti_interesse.models import PuntoInteresse, FotoAccessoria, ValidazionePunto, InteresseSpecifico

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

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        slug = slugify(nome)
        if PuntoInteresse.objects.exclude(id=self.instance.id).filter(slug=slug):
            raise forms.ValidationError("Nome già utilizzato.")
        return nome

    def clean(self):
        cleaned_data = super(PuntoInteresseForm, self).clean()
        visitabile = cleaned_data.get('visitabile')
        visitabile2 = cleaned_data.get('visitabile2')

        if not visitabile and visitabile2:
            raise forms.ValidationError("Il punto di interesse non può essere visitabile solo per persone con disabilità")

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
            'descr_estesa' : forms.Textarea(attrs={'rows':8, 'cols':40}),
            'descr_breve' : forms.Textarea(attrs={'rows':4, 'cols':40}),
            'descr_sito' : forms.Textarea(attrs={'rows':4, 'cols':40}),
            'motivo' : forms.Textarea(attrs={'rows':2, 'cols':40}),
            'rif_biblio' : forms.Textarea(attrs={'rows':2, 'cols':40}),
            'rif_sito' : forms.Textarea(attrs={'rows':2, 'cols':40}),
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
