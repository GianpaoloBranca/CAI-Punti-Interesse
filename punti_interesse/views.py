from django.shortcuts import render
from django.forms import modelformset_factory
from punti_interesse.models import PuntoInteresse, ValidazionePunto, FotoAccessoria
from punti_interesse.forms import PuntoInteresseForm, FotoAccessoriaForm

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
    context_dict['fotos'] = FotoAccessoria.objects.filter(punto=punto.id)
    return render(request, 'punti_interesse/pi.html', context_dict)

def edit_pi(request, pi_name_slug):

    punto = get_pi(pi_name_slug)
    fotos = FotoAccessoria.objects.filter(punto=punto.id)

    FotoFormSet = modelformset_factory(FotoAccessoria, form=FotoAccessoriaForm, extra=5, max_num=5, can_delete=True)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, files=request.FILES, instance=punto)

        fotoformset = FotoFormSet(request.POST, files=request.FILES, queryset=fotos)

        if form.is_valid() and fotoformset.is_valid():
            form.save(commit=True)
            # TODO hack
            for fotoform in fotoformset.cleaned_data:
                if fotoform:
                    foto = fotoform['foto']
                    if fotoform['id']:
                        foto_acc = FotoAccessoria.objects.get(id=fotoform['id'].id)
                        foto_acc.punto = punto
                        foto_acc.foto = foto
                    else:
                        foto_acc = FotoAccessoria(foto=foto, punto=punto)

                    if fotoform['DELETE']:
                        foto_acc.delete()
                    else:
                        foto_acc.save()

            return show_pi_ril(request, pi_name_slug)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['form'] = PuntoInteresseForm(instance=punto)
    # Il linter da un errore inesistente in questa riga
    context_dict['fotoformset'] = FotoFormSet(queryset=fotos)
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
