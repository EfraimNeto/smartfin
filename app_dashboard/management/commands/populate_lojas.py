# app_dashboard/management/commands/populate_lojas.py
from django.core.management.base import BaseCommand
from app_dashboard.models import Loja

LOJA_CHOICES = [
    ('BARBACOA', 'Barbacoa'),
    ('BARRA', 'Barra'),
    ('VILAS', 'Vilas'),
    ('SMART', 'Smart'),
    ('DIGITAL', 'Digital'),
    ('APP', 'App'),
]

class Command(BaseCommand):
    help = 'Popula o modelo Loja com opções predefinidas'

    def handle(self, *args, **kwargs):
        for code, name in LOJA_CHOICES:
            Loja.objects.get_or_create(nome=name)
        
        self.stdout.write(self.style.SUCCESS('Lojas populadas com sucesso'))
