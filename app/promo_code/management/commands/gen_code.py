from typing import Union
from django.core.management.base import BaseCommand

from promo_code.services import generate_promo_code


class Command(BaseCommand):
    help = "Генерирует ноыве промо коды и сохраняет их"

    def add_arguments(self, parser):
        parser.add_argument('-a',
                            '--amount',
                            type=int,
                            help="Количество новых кодов")

        parser.add_argument('-g',
                            '--group',
                            type=str,
                            help="Название группы, для которой будут созданы промокоды")


    def handle(self, *args, **kwargs):
        amount = kwargs['amount']
        group = kwargs['group']
        codes = generate_promo_code(amount, group)
        self.stdout.write(u'Новые коды: %s' % codes)

        