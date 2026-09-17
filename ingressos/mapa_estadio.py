"""
Desenho do mapa de setores do estádio (SVG).

Cada setor é um pedaço de um anel oval, definido por ângulo inicial e final:

0° = direita, 90° = embaixo, 180° = esquerda, 270° = em cima.

Os setores do banco são ligados ao desenho pelo NOME, sem diferenciar
maiúsculas e acentos: "Caldeirão", "caldeirao" e "CALDEIRÃO" funcionam.
"""

import math

from django.utils.text import slugify


CENTRO = (430, 280)

RAIO_EXTERNO = (350, 215)

RAIO_INTERNO = (245, 140)


# Portões: (rótulo, ângulo, distância para fora do anel)

GEOMETRIA = {

    "cadeiras": {
        "nome": "Cadeiras",
        "cor": "#2b3a8f",
        "inicio": 214,
        "fim": 312,
        "portoes": [
            ("64", 222, 26),
            ("A", 228, 58),
            ("63", 292, 26),
        ],
    },

    "caldeirao": {
        "nome": "Caldeirão",
        "cor": "#1f9a55",
        "inicio": 314,
        "fim": 374,
        "portoes": [],
    },

    "visitante": {
        "nome": "Visitante",
        "cor": "#f08a24",
        "inicio": 376,
        "fim": 418,
        "portoes": [
            ("68", 40, 26),
        ],
    },

    "vermelho": {
        "nome": "Vermelho",
        "cor": "#d7191c",
        "inicio": 64,
        "fim": 120,
        "portoes": [
            ("67", 88, 26),
            ("D", 83, 58),
            ("C", 97, 58),
        ],
    },

    "hexa": {
        "nome": "Hexa",
        "cor": "#f2d21b",
        "inicio": 136,
        "fim": 212,
        "portoes": [
            ("B", 191, 60),
            ("65", 196, 26),
            ("66", 184, 26),
        ],
    },

}


COR_INDISPONIVEL = "#9a9a9a"


def _ponto(angulo, rx, ry):

    t = math.radians(angulo)

    return (
        CENTRO[0] + rx * math.cos(t),
        CENTRO[1] + ry * math.sin(t)
    )


def _caminho(inicio, fim):

    rx, ry = RAIO_EXTERNO

    irx, iry = RAIO_INTERNO

    grande = 1 if fim - inicio > 180 else 0

    x1, y1 = _ponto(inicio, rx, ry)

    x2, y2 = _ponto(fim, rx, ry)

    x3, y3 = _ponto(fim, irx, iry)

    x4, y4 = _ponto(inicio, irx, iry)

    return (
        f"M {x1:.1f} {y1:.1f} "
        f"A {rx} {ry} 0 {grande} 1 {x2:.1f} {y2:.1f} "
        f"L {x3:.1f} {y3:.1f} "
        f"A {irx} {iry} 0 {grande} 0 {x4:.1f} {y4:.1f} Z"
    )


def _cor_do_texto(cor_hex):

    """
    Texto escuro em cores claras (ex.: amarelo),
    branco nas escuras.
    """

    r, g, b = (
        int(cor_hex[i:i + 2], 16)
        for i in (1, 3, 5)
    )

    luminancia = (
        0.299 * r +
        0.587 * g +
        0.114 * b
    ) / 255

    return "#1c1c1c" if luminancia > 0.6 else "#ffffff"


def _formatar_preco(valor):

    return (
        "R$ " +
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def montar_mapa(setores):

    """
    Recebe os setores de um jogo e devolve:

    - lista de setores prontos para desenhar no SVG
    - dicionário com os dados usados pelo JavaScript
    - nomes de setores esperados que não existem para esse jogo
    """

    do_banco = {
        slugify(s.nome): s
        for s in setores
    }

    desenho = []

    faltando = []


    for chave, geo in GEOMETRIA.items():

        setor = do_banco.get(chave)


        if setor is None:

            faltando.append(geo["nome"])

            disponivel = False

            situacao = "Indisponível"

            quantidade = 0

            setor_id = None

            nome = geo["nome"]

            preco = None


        else:

            disponivel = setor.quantidade > 0

            situacao = (
                _formatar_preco(setor.preco)
                if disponivel
                else "Esgotado"
            )

            quantidade = setor.quantidade

            setor_id = setor.id

            nome = setor.nome

            preco = _formatar_preco(setor.preco)


        cor = (
            geo["cor"]
            if disponivel
            else COR_INDISPONIVEL
        )


        meio = (
            geo["inicio"] + geo["fim"]
        ) / 2


        rotulo_x, rotulo_y = _ponto(

            meio,

            (
                RAIO_EXTERNO[0] +
                RAIO_INTERNO[0]
            ) / 2,

            (
                RAIO_EXTERNO[1] +
                RAIO_INTERNO[1]
            ) / 2,

        )


        portoes = []


        for rotulo, angulo, distancia in geo["portoes"]:

            x, y = _ponto(

                angulo,

                RAIO_EXTERNO[0] + distancia,

                RAIO_EXTERNO[1] + distancia

            )


            portoes.append({

                "rotulo": rotulo,

                "x": round(x, 1),

                "y": round(y, 1),

                "caixa_x": round(x - 15, 1),

                "caixa_y": round(y - 11, 1),

            })


        desenho.append({

            "chave": chave,

            "id": setor_id,

            "nome": nome,

            "cor": cor,

            "cor_texto": _cor_do_texto(cor),

            "caminho": _caminho(
                geo["inicio"],
                geo["fim"]
            ),

            "rotulo_x": round(rotulo_x, 1),

            "rotulo_y": round(rotulo_y, 1),

            "portoes": portoes,

            "situacao": situacao,

            "disponivel": disponivel,

        })


    dados_js = {

        s["chave"]: {

            "id": s["id"],

            "nome": s["nome"],

            "cor": s["cor"],

            "situacao": s["situacao"],

            "disponivel": s["disponivel"],

            "quantidade": (
                do_banco[s["chave"]].quantidade
                if s["id"]
                else 0
            ),

            "portoes": (
                ", ".join(
                    p["rotulo"]
                    for p in s["portoes"]
                )
                or "Consulte o clube"
            ),

        }

        for s in desenho

    }


    return desenho, dados_js, faltando


CONTEXTO_FIXO = {

    "centro_x": CENTRO[0],

    "centro_y": CENTRO[1],

    "gramado_rx": RAIO_INTERNO[0] - 8,

    "gramado_ry": RAIO_INTERNO[1] - 8,

}