from django.shortcuts import render
from .models import Jogo


def home(request):
    return render(request, 'ingressos/home.html')


def jogos(request):
    lista_jogos = Jogo.objects.all()

    return render(
        request,
        'ingressos/jogos.html',
        {'jogos': lista_jogos}
    )
# Create your views here.
