from django.shortcuts import render
from punti_interesse.models import PuntoInteresse

def index(request):
    return render(request, 'punti_interesse/index.html')

def rilevatore(request):
    lista_punti = PuntoInteresse.objects.order_by('data')
    return render(request, 'punti_interesse/rilevatore.html', {'punti': lista_punti})

def validatore(request):
    lista_punti = PuntoInteresse.objects.order_by('data')
    return render(request, 'punti_interesse/validatore.html', {'punti': lista_punti})
