from django.shortcuts import render

def home(request):
    return render(request, 'ingressos/home.html')

def jogos(request):
    return render(request, 'ingressos/jogos.html')

# Create your views here.
