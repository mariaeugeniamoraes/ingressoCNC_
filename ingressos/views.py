from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from .models import Jogo, Setor, Pedido
from .forms import CadastroForm, PerfilForm
from .mapa_estadio import montar_mapa, CONTEXTO_FIXO
from .ingresso_qr import gerar_codigo, ler_codigo, gerar_qr_svg


# Quantidade máxima de ingressos em um único pedido
MAX_INGRESSOS_POR_PEDIDO = 6


# ----------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------------

def erro(request, mensagem):
    """Atalho para a tela de erro da compra."""
    return render(
        request,
        'ingressos/erro_compra.html',
        {'mensagem': mensagem}
    )


def ler_quantidade(valor):
    """
    Converte o que veio do formulário em número.
    Se a pessoa mexer no HTML e mandar texto, devolve 0
    em vez de derrubar o site com erro 500.
    """
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0


def problema_na_compra(setor, quantidade):
    """
    Confere todas as regras de venda de uma vez.
    Devolve a mensagem de erro, ou None se estiver tudo certo.

    Essas mesmas regras são conferidas em cada etapa da compra,
    porque o navegador pode pular telas indo direto pela URL.
    """

    if setor.jogo.encerrado:
        return 'Este jogo já aconteceu. Não é mais possível comprar ingressos.'

    if setor.esgotado:
        return f'Os ingressos do setor {setor.nome} estão esgotados.'

    if quantidade < 1:
        return 'Escolha pelo menos um ingresso.'

    if quantidade > MAX_INGRESSOS_POR_PEDIDO:
        return (
            f'É possível comprar no máximo '
            f'{MAX_INGRESSOS_POR_PEDIDO} ingressos por pedido.'
        )

    if quantidade > setor.quantidade:
        return (
            f'Restam apenas {setor.quantidade} ingressos '
            f'no setor {setor.nome}.'
        )

    return None


# ----------------------------------------------------------------
# PÁGINAS PÚBLICAS
# ----------------------------------------------------------------

def home(request):
    return render(request, 'ingressos/home.html')


def jogos(request):
    """
    Lista as partidas. Os jogos que já aconteceram vão para o fim,
    e cada card mostra a situação: à venda, esgotado ou encerrado.
    """

    todos = Jogo.objects.prefetch_related('setor_set')

    proximos = [jogo for jogo in todos if not jogo.encerrado]
    encerrados = [jogo for jogo in todos if jogo.encerrado]

    return render(
        request,
        'ingressos/jogos.html',
        {
            'jogos': proximos,
            'encerrados': list(reversed(encerrados)),
        }
    )


# ----------------------------------------------------------------
# FLUXO DE COMPRA
# ----------------------------------------------------------------

@login_required(login_url='login')
def comprar(request, jogo_id):
    """Mapa de setores do jogo escolhido."""

    jogo = get_object_or_404(Jogo, id=jogo_id)

    if jogo.encerrado:
        return erro(
            request,
            'Este jogo já aconteceu. Não é mais possível comprar ingressos.'
        )

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


@login_required(login_url='login')
def selecionar_setor(request, setor_id):
    """Escolha da quantidade de ingressos."""

    setor = get_object_or_404(Setor, id=setor_id)

    if setor.jogo.encerrado:
        return erro(
            request,
            'Este jogo já aconteceu. Não é mais possível comprar ingressos.'
        )

    if setor.esgotado:
        return erro(
            request,
            f'Os ingressos do setor {setor.nome} estão esgotados.'
        )

    return render(
        request,
        'ingressos/selecionar_setor.html',
        {
            'setor': setor,
            'maximo': min(setor.quantidade, MAX_INGRESSOS_POR_PEDIDO),
        }
    )


@login_required(login_url='login')
def resumo(request, setor_id):
    """Resumo antes da verificação facial."""

    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = ler_quantidade(request.GET.get('quantidade', 1))

    mensagem = problema_na_compra(setor, quantidade)
    if mensagem:
        return erro(request, mensagem)

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
def verificacao_facial(request, setor_id):
    """Simulação da verificação de identidade."""

    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = ler_quantidade(
        request.POST.get('quantidade') or request.GET.get('quantidade')
    )

    mensagem = problema_na_compra(setor, quantidade)
    if mensagem:
        return erro(request, mensagem)

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
    """Escolha da forma de pagamento."""

    setor = get_object_or_404(Setor, id=setor_id)

    quantidade = ler_quantidade(
        request.POST.get('quantidade') or request.GET.get('quantidade')
    )

    mensagem = problema_na_compra(setor, quantidade)
    if mensagem:
        return erro(request, mensagem)

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


@login_required(login_url='login')
def finalizar_compra(request, setor_id):
    """Cria o pedido e desconta os ingressos do estoque."""

    # A finalização só pode acontecer por POST
    if request.method != 'POST':
        return redirect('jogos')

    quantidade = ler_quantidade(request.POST.get('quantidade', 1))

    forma_pagamento = request.POST.get('forma_pagamento')

    formas_validas = ['pix', 'credito', 'debito']

    if forma_pagamento not in formas_validas:
        return erro(request, 'Selecione uma forma de pagamento válida.')

    # transaction.atomic + select_for_update travam a linha do setor
    # durante a venda. Assim, duas pessoas comprando ao mesmo tempo
    # não conseguem levar o mesmo último ingresso.
    with transaction.atomic():

        setor = get_object_or_404(
            Setor.objects.select_for_update(),
            id=setor_id
        )

        mensagem = problema_na_compra(setor, quantidade)
        if mensagem:
            return erro(request, mensagem)

        # Calcula no servidor. Não confiamos no valor enviado pelo navegador.
        total = setor.preco * quantidade

        pedido = Pedido.objects.create(
            usuario=request.user,
            setor=setor,
            quantidade=quantidade,
            valor_total=total,
            biometria_verificada=True,
            forma_pagamento=forma_pagamento,
            status_pagamento='pago'
        )

        # Desconta usando F(), que faz a conta dentro do banco
        Setor.objects.filter(id=setor.id).update(
            quantidade=F('quantidade') - quantidade
        )

    return render(
        request,
        'ingressos/compra_finalizada.html',
        {'pedido': pedido}
    )


# ----------------------------------------------------------------
# CONTA DO USUÁRIO
# ----------------------------------------------------------------

def cadastro(request):

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()

            return render(
                request,
                'ingressos/cadastro_sucesso.html'
            )

    else:
        form = CadastroForm()

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

            # Só aceita endereços do próprio site.
            # Sem isso, um link como ?next=http://site-falso.com
            # levaria a pessoa para fora depois do login.
            if proxima_pagina and proxima_pagina.startswith('/'):
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
def perfil(request):
    """Dados da conta e resumo das compras."""

    pedidos = Pedido.objects.filter(usuario=request.user)

    return render(
        request,
        'ingressos/perfil.html',
        {
            'total_pedidos': pedidos.count(),
            'ultimo_pedido': pedidos.order_by('-data_compra').first(),
        }
    )


@login_required(login_url='login')
def editar_perfil(request):
    """Permite alterar nome, sobrenome e e-mail."""

    if request.method == 'POST':
        # instance=request.user garante que a pessoa só edita
        # a própria conta, não importa o que venha no formulário
        form = PerfilForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('perfil')

    else:
        form = PerfilForm(instance=request.user)

    return render(
        request,
        'ingressos/editar_perfil.html',
        {'form': form}
    )


@login_required(login_url='login')
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).select_related('setor', 'setor__jogo').order_by('-data_compra')

    return render(
        request,
        'ingressos/meus_pedidos.html',
        {'pedidos': pedidos}
    )


# ----------------------------------------------------------------
# INGRESSO E VALIDAÇÃO
# ----------------------------------------------------------------

@login_required(login_url='login')
def ingresso(request, pedido_id):
    """Ingresso virtual com QR Code."""

    # O filtro por usuário entra na própria busca: trocar o id na URL
    # devolve "página não encontrada", sem revelar que o pedido existe.
    if request.user.is_staff:
        pedido = get_object_or_404(Pedido, id=pedido_id)
    else:
        pedido = get_object_or_404(
            Pedido,
            id=pedido_id,
            usuario=request.user
        )

    codigo = gerar_codigo(pedido)

    endereco = request.build_absolute_uri(
        reverse('validar_ingresso', args=[codigo])
    )

    qr = gerar_qr_svg(endereco)

    return render(
        request,
        'ingressos/ingresso.html',
        {
            'pedido': pedido,
            'codigo': codigo,
            'endereco': endereco,
            'qr': qr,
        }
    )


@staff_member_required
def validar_ingresso(request, codigo):
    """
    Página usada pela equipe do clube na portaria.
    Lê o código do QR e diz se o ingresso é válido.
    """

    pedido_id = ler_codigo(codigo)

    pedido = None
    if pedido_id is not None:
        pedido = (
            Pedido.objects
            .select_related('setor', 'setor__jogo')
            .filter(id=pedido_id)
            .first()
        )

    return render(
        request,
        'ingressos/validar_ingresso.html',
        {'pedido': pedido}
    )