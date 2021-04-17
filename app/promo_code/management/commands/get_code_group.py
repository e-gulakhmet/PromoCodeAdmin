from os import path
from typing import Union
from django.core.management.base import BaseCommand

from promo_code.services import get_code_group
from promo_code.apps import PromoCodeConfig


class Command(BaseCommand):
    help = "Ищет группу по указанному коду."

    def add_arguments(self, parser):
        parser.add_argument('-c',
                            '--code',
                            type=str,
                            help="Код, по которому будет найдена группа")
        parser.add_argument("-p",
                            "--path",
                            type=str,
                            default=PromoCodeConfig.promo_codes_file_path,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        code = kwargs['code']
        path = kwargs["path"]

        if code is None or code == "" :
            self.stdout.write("Укажите код: -с <код>")
            return

        group = get_code_group(code, path)
        if group is None:
            self.stdout.write("код не существует")
            return
        self.stdout.write("код существует группа = {%s}" % group)