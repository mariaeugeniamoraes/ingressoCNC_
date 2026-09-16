from django.db import models
from django.contrib.auth.models import User


class Jogo(models.Model):
    adversario = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()
    estadio = models.CharField(max_length=100)

    def __str__(self):
        return f"Náutico x {self.adversario}"


class Setor(models.Model):
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nome} - {self.jogo}"

class Pedido(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.setor}"

# Create your models here.
