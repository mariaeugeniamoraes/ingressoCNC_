from django.shortcuts import render, get_object_or_404, redirect
from .models import Jogo, Setor, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .mapa_estadio import montar_mapa, CONTEXTO_FIXO

def home(request):
    return render(request, 'ingressos/home.html')


def jogos(request):
    lista_jogos = Jogo.objects.all()

    return render(
        request,
        'ingressos/jogos.html',
        {'jogos': lista_jogos}
    )

@login_required(login_url='login')
def comprar(request, jogo_id):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    setores = jogo.setor_set.all()

    mapa, dados_mapa, setores_faltando = montar_mapa(setores)

    return render(
        request,
        'ingressos/comprar.html',
        {
            'jogo': jogo,
            'setores': setores,
            'mapa': mapa,
            'dados_mapa': dados_mapa,
            'setores_faltando': setores_faltando,
            **CONTEXTO_FIXO,
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

@login_required(login_url='login')
def finalizar_compra(request, setor_id):

    setor = get_object_or_404(
        Setor,
        id=setor_id
    )

    # A finalização só pode acontecer por POST
    if request.method != 'POST':
        return redirect('jogos')

    quantidade = int(
        request.POST.get('quantidade', 1)
    )

    forma_pagamento = request.POST.get(
        'forma_pagamento'
    )

    # Verifica se a quantidade é válida
    if quantidade < 1 or quantidade > setor.quantidade:

        return render(
            request,
            'ingressos/erro_compra.html',
            {
                'mensagem':
                'Quantidade de ingressos inválida.'
            }
        )

    # Formas de pagamento aceitas na simulação
    formas_validas = [
        'pix',
        'credito',
        'debito'
    ]

    # Verifica se o usuário escolheu
    # uma forma de pagamento válida
    if forma_pagamento not in formas_validas:

        return render(
            request,
            'ingressos/erro_compra.html',
            {
                'mensagem':
                'Selecione uma forma de pagamento válida.'
            }
        )

    # Calcula novamente no servidor.
    # Não confiamos no valor enviado pelo navegador.
    total = setor.preco * quantidade

    # Cria o pedido
    pedido = Pedido.objects.create(

        usuario=request.user,

        setor=setor,

        quantidade=quantidade,

        valor_total=total,

        biometria_verificada=True,

        forma_pagamento=forma_pagamento,

        status_pagamento='pago'

    )

    # Desconta os ingressos vendidos
    setor.quantidade = (
        setor.quantidade - quantidade
    )

    setor.save()

    # Exibe a confirmação
    return render(
        request,
        'ingressos/compra_finalizada.html',
        {
            'pedido': pedido
        }
    )

def cadastro(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return render(
                request,
                'ingressos/cadastro_sucesso.html'
            )

    else:
        form = UserCreationForm()

    return render(
        request,
        'ingressos/cadastro.html',
        {'form': form}
    )

def entrar(request):
    mensagem = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)

            proxima_pagina = request.POST.get('next')

            if proxima_pagina:
                return redirect(proxima_pagina)

            return redirect('home')
        else:
            mensagem = 'Usuário ou senha incorretos.'

    return render(
        request,
        'ingressos/login.html',
        {'mensagem': mensagem}
    )

def sair(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-data_compra')

    return render(
        request,
        'ingressos/meus_pedidos.html',
        {'pedidos': pedidos}
    )

@login_required(login_url='login')
def verificacao_facial(request, setor_id):
    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = request.POST.get('quantidade')

    return render(
        request,
        'ingressos/verificacao_facial.html',
        {
            'setor': setor,
            'quantidade': quantidade
        }
    )

@login_required(login_url='login')
def pagamento(request, setor_id):

    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = int(request.POST.get('quantidade', 1))

    if quantidade < 1 or quantidade > setor.quantidade:

        return render(
            request,
            'ingressos/erro_compra.html',
            {
                'mensagem': 'Quantidade de ingressos inválida.'
            }
        )

    total = setor.preco * quantidade

    return render(
        request,
        'ingressos/pagamento.html',
        {
            'setor': setor,
            'quantidade': quantidade,
            'total': total
        }
    )
# Create your views here.