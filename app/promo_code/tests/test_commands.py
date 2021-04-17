import json
import os
from io import StringIO
import re

from django.test import TestCase
from django.core.management import call_command

from app.settings import BASE_DIR
from promo_code.services import generate_promo_code




class CommandsTestCase(TestCase):
    def test_cammand_gen_code(self):
        """
        Тест комманды, которая генерирует новые промо коды.
        """
        
        # Путь до тестового файла кодов
        file_path = os.path.join(BASE_DIR, "promo_code", "tests", "codes.json")
        # Удаляем файл с кодами, если он есть
        try:
            os.remove(file_path)
        except:
            pass

        # Запускаем команды
        call_command('gen_codes',**{"amount": 10,
                                    "group": "агенства",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 1,
                                    "group": "агенства",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 42,
                                    "group": "avtostop",
                                    "path": file_path})
        call_command('gen_codes',**{"amount": 5,
                                    "group": 1,
                                    "path": file_path})

        
        data = None
        with open(file_path) as file:
            data = json.load(file)
        # Находим количесво групп и кодов
        groups = []
        codes_count = 0
        for object in data["data"]:
            print(object)
            # Если название группы есть в списке уже найденных групп
            if object["group"] not in groups:
                # Если группы нет в списке найденных групп
                # Добавляем ее в этот список
                groups.append(object["group"])
            # Добавляем к числу кодов количество кодов этой группы
            codes_count += len(object["codes"])

        # Удаляем тестовый файл с кодами
        os.remove(file_path)

        self.assertEqual(len(groups), 3)
        self.assertEqual(codes_count, 58)



    def test_cammand_get_code(self):
        """
        Тест комманды, которая находит группу указанного кода.
        """
        
        # Путь до тестового файла кодов
        file_path = os.path.join(BASE_DIR, "promo_code", "tests", "codes.json")

        # Удаляем файл с кодами, если он есть
        try:
            os.remove(file_path)
        except:
            pass

        # Создаем файл с кодами
        generate_promo_code(amount=10, group="агенства", file_path=file_path)
        generate_promo_code(amount=10, group="агенства", file_path=file_path)
        codes = generate_promo_code(amount=10, group="avtostop", file_path=file_path)
        generate_promo_code(amount=10, group=1, file_path=file_path)

        out = StringIO()
        # Запускаем комманду, которая будет искать код файле
        call_command('get_code_group',
                     **{"code": codes[0],
                        "path": file_path},
                     stdout=out)

        # Удаляем тестовый файл с кодами
        os.remove(file_path)

        self.assertIsNotNone(re.search("avtostop", out.getvalue()))
