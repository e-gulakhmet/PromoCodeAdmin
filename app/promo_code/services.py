import json
from json.decoder import JSONDecodeError
import random
import os
from typing import Union
import logging

from .apps import PromoCodeConfig


logger = logging.getLogger(__name__)


def generate_promo_code(amount: int=1,
                        group: Union[int, str]="default",
                        file_path: str=PromoCodeConfig.promo_codes_file_path,
                        recreate: bool=False):
    """
    Генерирует рандомные промо коды.

    Parameters
    ----------
    amount: str
        Количество промо кодов, которые нужно сгенерировать.

    group: int, str
        Название группы, которой будет принадлежать промо код.

    file_path: str
        Путь к файлу, в котором будут лежать коды.

    recreate: bool
        Если True, пересоздает файл с кодами.

    Returns
    -------
    list
        Список с созданными промо кодами.
    """

    assert amount is not None and amount > 0, "Amount must be > 0"
    assert group is not None and group != "", "Group must be not empty str"
    assert file_path is not None, "File path must be str, not None"

    logger.debug(f"Generating new codes")
    logger.debug(f"Parameters: amount={amount}, group={group}, recreate={recreate}")

    symbols = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"

    random.seed()

    # Генерируем рандомные ключи
    codes = []
    for _ in range(amount):
        codes.append("".join(random.choices(symbols, k=random.randint(4, 15))))

    if recreate:
        logger.debug("Removing old file")
        try:
            os.remove(file_path)
        except FileNotFoundError:
            logger.debug('File not found')
        except Exception:
            pass

    # Если файл существует, то получаем данные из него
    logger.debug("Retrieving data from the old file")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    # Если файл не был найден или его содержимое пустое,
    # то создаем новый и записываем туда новые данные
    except (FileNotFoundError, JSONDecodeError):
        logger.debug("File not found")
        logger.debug("Uplaoding codes to new file")
        try:
            with open(file_path, "w") as file:
                json.dump(
                    {
                        "data": [
                            {
                                "group": group,
                                "codes": codes
                            }
                        ]
                    },
                    file,
                    ensure_ascii=False
                )
        except Exception as e:
            logger.warning("Failed to uplaod new codes: {e}")
        logger.debug("Codes uploaded")
        return codes

    logger.debug("Got data from old file")
    # Получаем все коды из файла
    file_codes = []
    for e in data["data"]:
        file_codes.extend(e["codes"])
    

    
    logger.debug("Checking new codes for repetition")
    i = 0
    # Проверяем сущесвует ли новый промо код в файле.
    while i < len(codes):
        if codes[i] not in file_codes:
            i += 1
            continue
        # Если такой код уже существует,
        # то удаляем этот код, создаем новый и проверяем его.
        logger.debug("Found a match")
        codes.pop(i)
        logger.debug("Replace with a new code")
        codes.insert(i, "".join(random.choices(symbols, k=random.randint(4, 15))))
    
    logger.debug("Uploading new codes")
    # Загружаем новую группу с кодами в файл
    try:
        with open(file_path, "r+") as file:
            bytes_count = os.path.getsize(file_path)
            file.seek(bytes_count - 2)
            file.write("," + json.dumps(
                {
                    "group": group,
                    "codes": codes
                }, ensure_ascii=False) + "]}"
            )
    except Exception as e:
        logger.warning(f"Failed to uplaod new codes: {e}")
    logger.debug("Codes uploaded")
    
    return codes



def get_code_group(code: str,
                   file_path: str=PromoCodeConfig.promo_codes_file_path):
    """
    Если указанный код был найден,
    возвращает навзавние группы.
    Иначе, если код не был найден,
    возварает None.

    Parameters
    ----------
    code: str
        Код, который нужно найти.

    file_path: str
        Путь к файлу, в котором будут лежать коды.

    Return
    ------
    str, None
    """
    
    assert code is not None, "Code must be str, not None"
    assert file_path is not None, "File path must be str, not None"

    logger.debug("Getting code gruop")
    logger.debug(f"Parameters: code={code}")

    # Получаем содержимое json файла, в котором храняться коды
    logger.debug("Retrieving data from the old file")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    # Если файл не был найден или его содержимое пустое,
    # то создаем новый и записываем туда новые данные
    except FileNotFoundError:
        logger.error("File not found")
        raise FileNotFoundError("File not found")
    except JSONDecodeError:
        logger.error("File not supported")
        raise ValueError("File not supported")

    logger.debug("Got data from file")
    
    logger.debug("Searching group by code")
    group = None
    # Проходимся по каждой группе
    for object in data["data"]:
        # Если встречаем одинаковые коды
        if code in object["codes"]:
        # Сохраняем название группы
            group = object["group"]
            break
    
    if group is None:
        logger.debug("Group not found")
        return None

    logger.debug(f"Found group: {group}")
    return group