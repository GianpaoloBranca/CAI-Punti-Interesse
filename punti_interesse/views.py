from django.shortcuts import render

def index(request):
    return render(request, 'punti_interesse/index.html')

def rilevatore(request):
    return render(request, 'punti_interesse/rilevatore.html')

def validatore(request):
    return render(request, 'punti_interesse/validatore.html')
