import json
from json.decoder import JSONDecodeError
import random
import os

from .apps import PromoCodeConfig


def generate_promo_code(amount: int=1, group="default"):
    """
    Генерирует рандомные промо коды.

    Parameters
    ----------
    amount: str
        Количество промо кодов, которые нужно сгенерировать.

    group: int, str
        Название группы, которой будет принадлежать промо код.

    Returns
    -------
    list
        Список с созданными промо кодами.
    """

    symbols = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"

    random.seed()

    # Генерируем рандомные ключи
    codes = []
    for _ in range(amount):
        codes.append("".join(random.choices(symbols, k=random.randint(4, 15))))
    
    # Если файл существует, то получаем данные из него
    try:
        with open(os.path.join(PromoCodeConfig.promo_codes_dir), "r") as file:
            data = json.load(file)
    # Если файл не был найден или его содержимое пустое,
    # то создаем новый и записываем туда новые данные
    except (FileNotFoundError, JSONDecodeError):
        with open(PromoCodeConfig.promo_codes_dir, "w") as file:
            json.dump(
                {
                    "data": [
                        {
                            "group": group,
                            "codes": codes
                        }
                    ]
                },
                file
            )
        return codes

    # Получаем все коды из файла
    file_codes = []
    for e in data["data"]:
        file_codes.extend(e["codes"])
    # Проверяем сущесвует ли новый промо код в файле.
    # Если такой код уже существует,
    # то удаляем этот код и создаем новый.
    for code in codes:
        if code not in file_codes:
            continue
        codes.remove(code)
        codes.append("".join(random.choices(symbols, k=random.randint(4, 15))))
    
    # Загружаем новую группу с кодами в файл
    with open(PromoCodeConfig.promo_codes_dir, "r+") as file:
        bytes_count = os.path.getsize(PromoCodeConfig.promo_codes_dir)
        file.seek(bytes_count - 2)
        file.write("," + json.dumps(
            {
                "group": group,
                "codes": codes
            },) + "]}"
        )
    
    return codes



def get_code_group(code: str):
    """
    Если указанной код был найден,
    возвращает: "код существует группа = {group}"
    Иначе, если код не был найден,
    пишет: "код не существует"

    Parameters
    ----------
    code: str
        Код, который нужно найти.

    Return
    ------
    str
    """

    # Получаем содержимое json файла, в котором храняться коды
    try:
        with open("promo_codes.json", "r") as file:
            data = json.load(file)
    # Если файл не был найден или его содержимое пустое,
    # то создаем новый и записываем туда новые данные
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    except JSONDecodeError:
        raise ValueError("File not supported")
    
    group = None
    # Проходимся по каждой группе
    for object in data["data"]:
        # Если встречаем одинаковые коды
        if code in object["codes"]:
        # Сохраняем название группы
            group = object["group"]
            break
    
    if group is None:
        return "код не существует"
    else:
        return "код существует группа = {" + group + "}"