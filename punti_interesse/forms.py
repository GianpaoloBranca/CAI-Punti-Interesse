from django import forms
from django.contrib.auth.models import User
from punti_interesse.models import PuntoInteresse, FotoAccessoria, ValidazionePunto

class PuntoInteresseForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    latitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)
    longitudine = forms.DecimalField(max_value=180, min_value=-180, max_digits=9, decimal_places=6)

    class Meta:
        model = PuntoInteresse
        fields = [
            'nome',
            'categoria',
            'tipo',
            'longitudine',
            'latitudine',
            'localita',
            'valle',
            'qualita',
            'estensione',
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
        ]

class FotoAccessoriaForm(forms.ModelForm):

    class Meta:
        model = FotoAccessoria
        fields = ('foto',)

class ValidazioneForm(forms.ModelForm):
    quota = forms.IntegerField(min_value=0)

    class Meta:
        model = ValidazionePunto
        fields = [
            'regione',
            'comunita_montana',
            'gruppo_montuoso',
            'quota',
            'descrizione',
        ]

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password',)
