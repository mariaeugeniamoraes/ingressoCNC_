from datetime import datetime, time

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone


class Jogo(models.Model):

    adversario = models.CharField(max_length=100)

    data = models.DateField()

    horario = models.TimeField(
        null=True,
        blank=True
    )

    estadio = models.CharField(max_length=100)

    class Meta:
        ordering = ["data", "horario"]

    def __str__(self):
        return f"Náutico x {self.adversario}"

    # ------------------------------------------------ estados do jogo
    # São propriedades, ou seja, calculadas na hora.
    # Não criam campo novo no banco e não pedem migração.

    @property
    def data_hora(self):
        """Data e horário juntos. Sem horário, considera meia-noite."""
        return datetime.combine(self.data, self.horario or time(0, 0))

    @property
    def encerrado(self):
        """O jogo já aconteceu?"""
        agora = timezone.localtime().replace(tzinfo=None)
        return self.data_hora < agora

    @property
    def ingressos_disponiveis(self):
        """Soma dos ingressos que ainda restam em todos os setores."""
        total = self.setor_set.aggregate(total=Sum("quantidade"))["total"]
        return total or 0

    @property
    def esgotado(self):
        return self.setor_set.exists() and self.ingressos_disponiveis == 0

    @property
    def disponivel(self):
        """Só um jogo disponível aceita novas compras."""
        return not self.encerrado and not self.esgotado

    @property
    def situacao(self):
        """Texto curto usado nas telas: encerrado, esgotado ou à venda."""
        if self.encerrado:
            return "encerrado"
        if self.esgotado:
            return "esgotado"
        return "disponivel"


class Setor(models.Model):

    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE
    )

    nome = models.CharField(max_length=100)

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} - {self.jogo}"

    @property
    def esgotado(self):
        return self.quantidade == 0

    @property
    def disponivel(self):
        return not self.esgotado and not self.jogo.encerrado


class Pedido(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    setor = models.ForeignKey(
        Setor,
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField()

    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_compra = models.DateTimeField(
        auto_now_add=True
    )

    biometria_verificada = models.BooleanField(
        default=False
    )

    # FORMAS DE PAGAMENTO

    FORMAS_PAGAMENTO = [
        ("pix", "PIX"),
        ("credito", "Cartão de crédito"),
        ("debito", "Cartão de débito"),
    ]

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO,
        blank=True
    )

    # STATUS DO PAGAMENTO

    STATUS_PAGAMENTO = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
    ]

    status_pagamento = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO,
        default="pendente"
    )

    def __str__(self):
        return f"Pedido {self.id} - {self.setor}"