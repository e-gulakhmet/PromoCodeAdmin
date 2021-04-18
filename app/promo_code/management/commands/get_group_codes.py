from typing import Union

from django.core.management.base import BaseCommand

from promo_code.services import get_codes_by_group
from promo_code.apps import PromoCodeConfig


class Command(BaseCommand):
    help = "Ищет коды по указанной группе."

    def add_arguments(self, parser):
        parser.add_argument('-g',
                            '--group',
                            type=str,
                            help="Код, по которому будет найдена группа")
        parser.add_argument("-p",
                            "--path",
                            type=str,
                            default=PromoCodeConfig.promo_codes_file_path,
                            help="Путь к файлу с кодами")


    def handle(self, *args, **kwargs):
        group = kwargs['group']
        path = kwargs["path"]

        if group is None or group == "" :
            self.stdout.write("Укажите группу: -g <группа>")
            return

        try:
            codes = get_codes_by_group(group, path)
        except FileNotFoundError:
            self.stdout.write("Файл не найден")
            self.stdout.write("Проверьте путь к файлу")
            return
        except ValueError:
            self.stdout.write("Не получается получить данные из файла")
            self.stdout.write("Проверьте содержимое файла")
            return
        except AssertionError:
            self.stdout.write("Неверно указаны параметры комманды")
            return

        if codes is None:
            self.stdout.write(f"Не удалось найти группу {group}")
            return
        self.stdout.write(f"Коды: {codes}")