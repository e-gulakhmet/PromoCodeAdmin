from typing import Union
from django.core.management.base import BaseCommand

from promo_code.services import generate_promo_code


class Command(BaseCommand):
    help = "Генерирует ноыве промо коды и сохраняет их."

    def add_arguments(self, parser):
        parser.add_argument("-a",
                            "--amount",
                            type=int,
                            help="Количество новых кодов")
        parser.add_argument("-g",
                            "--group",
                            type=str,
                            help="Название группы, для которой будут созданы промокоды")
        parser.add_argument("-r",
                            "--recreate",
                            action="store_true",
                            help="Пересоздать файл с кодами")
        parser.add_argument("-p",
                            "--path",
                            type=str,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        amount = kwargs["amount"]
        group = kwargs["group"]
        recreate = kwargs["recreate"]
        file_path = kwargs["path"]
        codes = generate_promo_code(amount=amount,
                                    group=group,
                                    recreate=recreate,
                                    file_path=file_path)
        self.stdout.write(f"Новые коды: {codes}")