from django import forms
from punti_interesse.models import PuntoInteresse, FotoAccessoria

class PuntoInteresseForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    data = forms.DateField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PuntoInteresse
        fields = [
            'longitudine',
            'latitudine',
            'categoria',
            'tipo',
            'nome',
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
        fields = [
            'foto',
        ]
