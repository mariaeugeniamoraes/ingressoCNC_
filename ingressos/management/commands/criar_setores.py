from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError

from ingressos.models import Jogo, Setor

# Preços e quantidades são VALORES DE EXEMPLO: ajuste pelo admin depois.
PADRAO = [
    ("Social", Decimal("80.00"), 4000),
    ("Hexa", Decimal("50.00"), 5000),
    ("Vermelho", Decimal("40.00"), 4500),
    ("Caldeirão", Decimal("30.00"), 4000),
    ("Visitante", Decimal("60.00"), 1500),
]


class Command(BaseCommand):
    help = "Cria os 5 setores do mapa para um jogo. Uso: python manage.py criar_setores <id_do_jogo>"

    def add_arguments(self, parser):
        parser.add_argument("jogo_id", type=int)

    def handle(self, *args, **options):
        try:
            jogo = Jogo.objects.get(pk=options["jogo_id"])
        except Jogo.DoesNotExist:
            raise CommandError(f"Não existe jogo com id {options['jogo_id']}")

        for nome, preco, quantidade in PADRAO:
            _, criado = Setor.objects.get_or_create(
                jogo=jogo,
                nome=nome,
                defaults={"preco": preco, "quantidade": quantidade},
            )
            situacao = "criado" if criado else "já existia"
            self.stdout.write(f"{nome}: {situacao}")

        self.stdout.write(self.style.SUCCESS(f"Setores prontos para {jogo}"))