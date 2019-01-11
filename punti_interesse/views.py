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

def show_pi_ril(request, pi_name_slug):
    context_dict = {}
    try:
        punto_interesse = PuntoInteresse.objects.get(slug=pi_name_slug)
        context_dict['punto'] = punto_interesse
    except PuntoInteresse.DoesNotExist:
        context_dict['punto'] = None
    return render(request, 'punti_interesse/pi.html', context_dict)
