from django.shortcuts import render
from punti_interesse.models import PuntoInteresse, ValidazionePunto
from punti_interesse.forms import PuntoInteresseForm

def index(request):
    return render(request, 'punti_interesse/index.html')

def rilevatore(request):
    lista_punti = PuntoInteresse.objects.order_by('data')
    return render(request, 'punti_interesse/rilevatore.html', {'punti': lista_punti})

def validatore(request):
    # TODO è solo una copia della pagina del rilevatore al momento
    lista_punti = PuntoInteresse.objects.order_by('data')
    return render(request, 'punti_interesse/validatore.html', {'punti': lista_punti})

def show_pi_ril(request, pi_name_slug):
    punto = get_pi(pi_name_slug)
    context_dict = {}
    context_dict['punto'] = punto
    context_dict['val'] = get_val(punto)
    return render(request, 'punti_interesse/pi.html', context_dict)

def edit_pi(request, pi_name_slug):

    punto = get_pi(pi_name_slug)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, instance=punto)

        if form.is_valid():
            form.save(commit=True)
            return show_pi_ril(request, pi_name_slug)


    context_dict = {}
    context_dict['punto'] = punto
    context_dict['form'] = PuntoInteresseForm(instance=punto)
    return render(request, 'punti_interesse/edit-pi.html', context_dict)

#______________________________________________________________________________

def get_pi(pi_name_slug):
    try:
        return PuntoInteresse.objects.get(slug=pi_name_slug)
    except PuntoInteresse.DoesNotExist:
        return None

def get_val(pi):
    try:
        return ValidazionePunto.objects.get(punto=pi.id)
    except ValidazionePunto.DoesNotExist:
        return None
