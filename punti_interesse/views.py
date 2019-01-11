from django.shortcuts import render

def index(request):
    return render(request, 'punti_interesse/index.html')
