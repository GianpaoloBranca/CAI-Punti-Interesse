from django import forms
from punti_interesse.models import PuntoInteresse

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
            'motivo'
        ]
