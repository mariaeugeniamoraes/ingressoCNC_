from django.db import models

class Jogo(models.Model):
    adversario = models.CharField(max_length=100)
    data = models.DateField()
    horario = models.TimeField()
    estadio = models.CharField(max_length=100)

    def __str__(self):
        return f"Náutico x {self.adversario}"

# Create your models here.
