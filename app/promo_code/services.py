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