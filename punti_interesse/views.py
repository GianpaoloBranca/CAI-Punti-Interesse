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
    context_dict['punto'] = get_pi(pi_name_slug)
    return render(request, 'punti_interesse/pi.html', context_dict)

def edit_pi(request, pi_name_slug):
    context_dict = {}
    context_dict['punto'] = get_pi(pi_name_slug)
    return render(request, 'punti_interesse/edit-pi.html', context_dict)

#______________________________________________________________________________

def get_pi(pi_name_slug):
    try:
        return PuntoInteresse.objects.get(slug=pi_name_slug)
    except PuntoInteresse.DoesNotExist:
        return None
