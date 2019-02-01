from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from punti_interesse.models import PuntoInteresse, ValidazionePunto, FotoAccessoria
from punti_interesse.forms import PuntoInteresseForm, FotoAccessoriaForm, ValidazioneForm
from punti_interesse.templatetags.pi_template_tags import is_rilevatore, is_validatore

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('home'))

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'punti_interesse/login.html')

@login_required
def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def home(request):
    lista_punti = PuntoInteresse.objects.order_by('data')
    return render(request, 'punti_interesse/home.html', {'punti': lista_punti})

@login_required
def show(request, slug):
    punto = get_pi(slug)

    if not punto:
        return render(request, '404.html', status=404)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['val'] = get_val(punto)
    context_dict['fotos'] = FotoAccessoria.objects.filter(punto=punto.id)
    return render(request, 'punti_interesse/show.html', context_dict)

@login_required
@user_passes_test(is_rilevatore)
def new(request):

    FotoFormSet = modelformset_factory(FotoAccessoria, form=FotoAccessoriaForm, extra=5, max_num=5)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, files=request.FILES)
        # pylint: disable=E1123
        fotoformset = FotoFormSet(request.POST, files=request.FILES, queryset=FotoAccessoria.objects.none())

        if form.is_valid() and fotoformset.is_valid():
            form.save(commit=True)
            punto = PuntoInteresse.objects.get(nome=form.cleaned_data['nome'])
            save_fotos(fotoformset, punto)
            return HttpResponseRedirect(reverse('show', kwargs={'slug': punto.slug}))

    else:
        form = PuntoInteresseForm()
        # pylint: disable=E1123
        fotoformset = FotoFormSet(queryset=FotoAccessoria.objects.none())

    context_dict = {}
    context_dict['form'] = form
    context_dict['fotoformset'] = fotoformset
    return render(request, 'punti_interesse/new.html', {'form' : form, 'fotoformset' : fotoformset})

@login_required
@user_passes_test(is_rilevatore)
def edit(request, slug):

    punto = get_pi(slug)
    fotos = FotoAccessoria.objects.filter(punto=punto.id)

    FotoFormSet = modelformset_factory(FotoAccessoria, form=FotoAccessoriaForm, extra=5, max_num=5, can_delete=True)

    if request.method == 'POST':
        form = PuntoInteresseForm(request.POST, files=request.FILES, instance=punto)
        # pylint: disable=E1123
        fotoformset = FotoFormSet(request.POST, files=request.FILES, queryset=fotos)

        if form.is_valid() and fotoformset.is_valid():
            punto = form.save(commit=False)
            punto.validato = False
            punto.save()
            save_fotos(fotoformset, punto)
            return HttpResponseRedirect(reverse('show', kwargs={'slug': punto.slug}))
    else:
        form = PuntoInteresseForm(instance=punto)
        # pylint: disable=E1123
        fotoformset = FotoFormSet(queryset=fotos)

    context_dict = {}
    context_dict['punto'] = punto
    context_dict['form'] = form
    context_dict['fotoformset'] = fotoformset
    return render(request, 'punti_interesse/edit.html', context_dict)

@login_required
@user_passes_test(is_validatore)
def validate(request, slug):
    punto = get_pi(slug)
    
    if not punto:
        render(request, '404.html', status=404)

    val = get_val(punto)

    if request.method == 'POST':
        form = ValidazioneForm(request.POST, instance=val)
        if form.is_valid():
            val = form.save(commit=False)
            val.punto = punto
            val.validatore = request.user.username
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

def handler404(request):
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

# TODO hack
def save_fotos(fotoformset, punto):
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
