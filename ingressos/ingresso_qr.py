"""
Ingresso virtual com QR Code.

O QR Code guarda o endereço de validação do ingresso, com um código
assinado pelo Django. A assinatura usa a SECRET_KEY do projeto, então
ninguém consegue inventar um código válido sem ter essa chave.

Nada disso precisa de campo novo no banco: o código é gerado a partir
do id do pedido e conferido na hora da leitura.
"""

import qrcode
from django.core import signing

SAL = "ingresso-nautico"

# Quanto tempo o código continua válido (2 dias, em segundos)
VALIDADE_SEGUNDOS = 60 * 60 * 48


def gerar_codigo(pedido):
    """Transforma o pedido em um código assinado."""
    return signing.dumps({"pedido": pedido.id}, salt=SAL)


def ler_codigo(codigo):
    """
    Devolve o id do pedido, ou None se o código for falso ou estiver vencido.
    """
    try:
        dados = signing.loads(codigo, salt=SAL, max_age=VALIDADE_SEGUNDOS)
    except signing.SignatureExpired:
        return None
    except signing.BadSignature:
        return None
    return dados.get("pedido")


def gerar_qr_svg(texto, tamanho_modulo=6):
    """
    Desenha o QR Code como SVG, sem precisar salvar imagem no servidor.

    O QR é uma grade de quadradinhos (chamados de módulos). Os quadrados
    pretos viram um único caminho (path) no SVG, o que deixa o arquivo pequeno.
    """
    qr = qrcode.QRCode(
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(texto)
    qr.make(fit=True)

    grade = qr.get_matrix()
    lado = len(grade) * tamanho_modulo

    partes = []
    for linha_indice, linha in enumerate(grade):
        for coluna_indice, escuro in enumerate(linha):
            if escuro:
                x = coluna_indice * tamanho_modulo
                y = linha_indice * tamanho_modulo
                partes.append(f"M{x} {y}h{tamanho_modulo}v{tamanho_modulo}h-{tamanho_modulo}z")

    return {
        "lado": lado,
        "caminho": "".join(partes),
    }