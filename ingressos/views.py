from django.shortcuts import render, get_object_or_404
from .models import Jogo, Setor, Pedido


def home(request):
    return render(request, 'ingressos/home.html')


def jogos(request):
    lista_jogos = Jogo.objects.all()

    return render(
        request,
        'ingressos/jogos.html',
        {'jogos': lista_jogos}
    )

def comprar(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    setores = jogo.setor_set.all()

    return render(
        request,
        'ingressos/comprar.html',
        {
            'jogo': jogo,
            'setores': setores
        }
    )

def selecionar_setor(request, setor_id):
    setor = get_object_or_404(Setor, id=setor_id)

    return render(
        request,
        'ingressos/selecionar_setor.html',
        {'setor': setor}
    )

def resumo(request, setor_id):
    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = int(request.GET.get('quantidade', 1))

    total = setor.preco * quantidade

    return render(
        request,
        'ingressos/resumo.html',
        {
            'setor': setor,
            'quantidade': quantidade,
            'total': total
        }
    )

def finalizar_compra(request, setor_id):
    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = int(request.POST.get('quantidade', 1))

    if quantidade < 1 or quantidade > setor.quantidade:
        return render(
            request,
            'ingressos/erro_compra.html',
            {'mensagem': 'Quantidade de ingressos inválida.'}
        )

    total = setor.preco * quantidade

    pedido = Pedido.objects.create(
        setor=setor,
        quantidade=quantidade,
        valor_total=total
    )

    setor.quantidade = setor.quantidade - quantidade
    setor.save()

    return render(
        request,
        'ingressos/compra_finalizada.html',
        {'pedido': pedido}
    )
# Create your views here.
