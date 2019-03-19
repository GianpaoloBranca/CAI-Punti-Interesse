from django import forms
from django.contrib.auth.models import User

from punti_interesse.models import PuntoInteresse, FotoAccessoria, ValidazionePunto, InteresseSpecifico
from custom_widgets.widgets import CountableTextArea

class PuntoInteresseForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    latitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)
    longitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)

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
            'descr_estesa'  : CountableTextArea(attrs={'rows':8, 'cols':40}),
            'descr_breve'   : CountableTextArea(attrs={'rows':4, 'cols':40}),
            'descr_sito'    : CountableTextArea(attrs={'rows':4, 'cols':40}),
            'motivo'        : CountableTextArea(attrs={'rows':4, 'cols':40}),
            'rif_biblio'    : CountableTextArea(attrs={'rows':4, 'cols':40}),
            'rif_sito'      : CountableTextArea(attrs={'rows':4, 'cols':40})
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
