import csv
from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, StreamingHttpResponse
from punti_interesse.models import PuntoInteresse, ValidazionePunto, FotoAccessoria, InteresseSpecifico, UserInfo
from punti_interesse.forms import PuntoInteresseForm, FotoAccessoriaForm, ValidazioneForm
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore
from punti_interesse.utils import Echo, csv_iterator


@login_required
def home(request):
    lista_punti = PuntoInteresse.objects.order_by('data')
    n_valid = lista_punti.count()
    n_invalid = PuntoInteresse.objects.filter(validato=False).count()
    return render(request, 'punti_interesse/home.html', {'punti': lista_punti, 'n_valid': n_valid, 'n_invalid': n_invalid})

@login_required
def show(request, slug):
    punto = get_pi(slug)

    if not punto:
        return render(request, '404.html', status=404)

    val = get_val(punto)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['val'] = val
    context_dict['fotos'] = FotoAccessoria.objects.filter(punto=punto.id)
    try:
        context_dict['ril_owner'] = punto.rilevatore.extra.uuid == request.user.extra.uuid
    except (AttributeError, UserInfo.DoesNotExist):
        context_dict['ril_owner'] = False
    return render(request, 'punti_interesse/show.html', context_dict)

@login_required
def new(request):

    if not is_rilevatore(request.user):
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')

    FotoFormSet = modelformset_factory(FotoAccessoria, form=FotoAccessoriaForm, extra=5, max_num=5)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, files=request.FILES)
        # pylint: disable=unexpected-keyword-arg
        fotoformset = FotoFormSet(request.POST, files=request.FILES, queryset=FotoAccessoria.objects.none())

        if form.is_valid() and fotoformset.is_valid():
            punto = form.save(commit=False)
            punto.rilevatore = request.user
            punto.save()
            save_fotos(fotoformset, punto)
            return HttpResponseRedirect(reverse('show', kwargs={'slug': punto.slug}))

    else:
        form = PuntoInteresseForm()
        # pylint: disable=unexpected-keyword-arg
        fotoformset = FotoFormSet(queryset=FotoAccessoria.objects.none())

    context_dict = {}
    context_dict['form'] = form
    context_dict['fotoformset'] = fotoformset
    return render(request, 'punti_interesse/new.html', {'form' : form, 'fotoformset' : fotoformset})

@login_required
def edit(request, slug):

    if not is_rilevatore(request.user):
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')

    punto = get_pi(slug)

    if not punto:
        return render(request, '404.html', status=404)

    try:
        if punto.rilevatore.extra.uuid != request.user.extra.uuid:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    except (AttributeError, UserInfo.DoesNotExist):
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')

    fotos = FotoAccessoria.objects.filter(punto=punto.id)

    FotoFormSet = modelformset_factory(FotoAccessoria, form=FotoAccessoriaForm, extra=5, max_num=5, can_delete=True)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, files=request.FILES, instance=punto)
        # pylint: disable=unexpected-keyword-arg
        fotoformset = FotoFormSet(request.POST, files=request.FILES, queryset=fotos)

        if form.is_valid() and fotoformset.is_valid():
            punto = form.save(commit=False)
            punto.validato = False
            punto.save()
            save_fotos(fotoformset, punto)
            return HttpResponseRedirect(reverse('show', kwargs={'slug': punto.slug}))
    else:
        form = PuntoInteresseForm(instance=punto)
        # pylint: disable=unexpected-keyword-arg
        fotoformset = FotoFormSet(queryset=fotos)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['form'] = form
    context_dict['fotoformset'] = fotoformset
    return render(request, 'punti_interesse/edit.html', context_dict)

@login_required
def validate(request, slug):

    if not is_validatore(request.user):
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')

    punto = get_pi(slug)

    if not punto:
        return render(request, '404.html', status=404)

    val = get_val(punto)

    if request.method == 'POST':
        form = ValidazioneForm(request.POST, instance=val)
        if form.is_valid():
            val = form.save(commit=False)
            val.punto = punto
            val.validatore = request.user
            val.save()
            punto.validato = True
            punto.save()
            return HttpResponseRedirect(reverse('show', kwargs={'slug': punto.slug}))
    else:
        form = ValidazioneForm(instance=val)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['form'] = form
    return render(request, 'punti_interesse/validate.html', context_dict)

@staff_member_required
def export_csv(request):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in csv_iterator()), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="punti.csv"'
    return response

@staff_member_required
def remove_invalid_points(request):
    PuntoInteresse.objects.filter(validato=False).delete()
    return HttpResponseRedirect(reverse('home'))

def load_subcategories(request):
    categoria = request.GET.get('categoria', -1)
    try:
        sottocategorie = InteresseSpecifico.objects.filter(tipo=categoria)
    except ValueError:
        sottocategorie = InteresseSpecifico.objects.none()
    return render(request, 'punti_interesse/form_subcategory.html', {'sottocategorie' : sottocategorie})

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

#______________________________________________________________________________

def get_pi(slug):
    try:
        return PuntoInteresse.objects.get(slug=slug)
    except PuntoInteresse.DoesNotExist:
        return None

def get_val(punto):
    try:
        return ValidazionePunto.objects.get(punto=punto.id)
    except ValidazionePunto.DoesNotExist:
        return None

def save_fotos(fotoformset, punto):
    fotos = fotoformset.save(commit=False)

    for foto in fotoformset.deleted_objects:
        foto.delete()

    for foto_acc in fotos:
        foto_acc.punto = punto
        foto_acc.save()
