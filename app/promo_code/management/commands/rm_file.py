from django.core.management.base import BaseCommand

from promo_code.services import remove_code_file
from promo_code.apps import PromoCodeConfig


class Command(BaseCommand):
    help = "Удаляет указанный файл с кодами."

    def add_arguments(self, parser):
        parser.add_argument("-p",
                            "--path",
                            type=str,
                            default=PromoCodeConfig.promo_codes_file_path,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        file_path = kwargs["path"]

        try:
            codes = remove_code_file(file_path)
        except FileNotFoundError:
            self.stdout.write("Файл не найден, проверьте путь к файлу")
            return
        self.stdout.write("Removed")