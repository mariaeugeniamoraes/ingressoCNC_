from datetime import date, time

from django.core.management.base import BaseCommand

from ingressos.models import Jogo


JOGOS = [
    {
        "adversario": "Sport Recife",
        "data": date(2026, 9, 26),
        "horario": time(16, 30),
    },
    {
        "adversario": "Grêmio Novorizontino",
        "data": date(2026, 10, 6),
        "horario": None,
    },
    {
        "adversario": "Vila Nova",
        "data": date(2026, 10, 11),
        "horario": time(17, 30),
    },
    {
        "adversario": "Avaí",
        "data": date(2026, 10, 31),
        "horario": None,
    },
    {
        "adversario": "CRB",
        "data": date(2026, 11, 7),
        "horario": None,
    },
]


class Command(BaseCommand):

    help = "Cadastra os próximos jogos do Náutico em casa."

    def handle(self, *args, **options):

        for dados in JOGOS:

            jogo, criado = Jogo.objects.update_or_create(
                adversario=dados["adversario"],
                data=dados["data"],
                defaults={
                    "horario": dados["horario"],
                    "estadio": "Estádio dos Aflitos",
                },
            )

            situacao = "criado" if criado else "atualizado"

            self.stdout.write(
                f"{jogo} - {situacao}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Jogos cadastrados com sucesso!"
            )
        )