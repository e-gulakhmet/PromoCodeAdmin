from typing import Union

from django.core.management.base import BaseCommand

from promo_code.services import generate_promo_code
from promo_code.apps import PromoCodeConfig


class Command(BaseCommand):
    help = "Генерирует ноыве промо коды и сохраняет их в указанный файл."

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
                            default=PromoCodeConfig.promo_codes_file_path,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        amount = kwargs["amount"]
        group = kwargs["group"]
        recreate = kwargs["recreate"]
        file_path = kwargs["path"]

        if amount is None :
            self.stdout.write("Укажите количество кодов: -a <количество>")
            return
        if group is None or group == "":
            self.stdout.write("Укажите группу: -g <группа>")
            return

        try:
            codes = generate_promo_code(amount=amount,
                                        group=group,
                                        recreate=recreate,
                                        file_path=file_path)
        except FileNotFoundError:
            self.stdout.write("Файл не найден, проверьте путь к файлу")
            return
        except AssertionError:
            self.stdout.write("Неверно указаны параметры команды")
            return
        self.stdout.write(f"Новые коды: {codes}")