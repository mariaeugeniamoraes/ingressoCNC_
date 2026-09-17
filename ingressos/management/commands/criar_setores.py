from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from ingressos.models import Jogo, Setor


# Setores e preços dos ingressos
PADRAO = [
    ("Vermelho", Decimal("80.00"), 4500),
    ("Hexa", Decimal("60.00"), 5000),
    ("Caldeirão", Decimal("60.00"), 4000),
    ("Cadeiras", Decimal("120.00"), 4000),
    ("Visitante", Decimal("100.00"), 1500),
]


class Command(BaseCommand):

    help = (
        "Cria ou atualiza os 5 setores do mapa para um jogo. "
        "Uso: python manage.py criar_setores <id_do_jogo>"
    )


    def add_arguments(self, parser):

        parser.add_argument(
            "jogo_id",
            type=int
        )


    def handle(self, *args, **options):

        try:

            jogo = Jogo.objects.get(
                pk=options["jogo_id"]
            )

        except Jogo.DoesNotExist:

            raise CommandError(
                f"Não existe jogo com id {options['jogo_id']}"
            )


        for nome, preco, quantidade in PADRAO:

            setor, criado = Setor.objects.update_or_create(

                jogo=jogo,

                nome=nome,

                defaults={
                    "preco": preco,
                    "quantidade": quantidade,
                },

            )


            situacao = (
                "criado"
                if criado
                else "atualizado"
            )


            self.stdout.write(
                f"{nome}: {situacao} - R$ {preco}"
            )


        self.stdout.write(

            self.style.SUCCESS(
                f"Setores prontos para {jogo}"
            )

        )