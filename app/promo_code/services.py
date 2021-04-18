import json
from json.decoder import JSONDecodeError
import random
import os
from typing import Union
import logging
import re

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
    assert file_path is not None and file_path != "", "File path must be str, not None"
    assert re.search(".json", file_path), "File must be in json format"

    logger.debug(f"Generating new codes")
    logger.debug(f"Parameters: amount={amount}, group={group}, recreate={recreate}")

    symbols = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"

    random.seed()

    # Генерируем рандомные ключи
    codes = []
    i = 0
    while i < amount:
        new_code = "".join(random.choices(symbols, k=random.randint(4, 15)))
        if new_code in codes:
            continue
        codes.append(new_code)
        i += 1

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
    
    logger.debug("Checking new codes for repeat")
    i = 0
    # Проверяем сущесвует ли новый промо код в файле.
    while i < len(codes):
        if codes[i] not in file_codes:
            i += 1
            continue
        # Если такой код уже существует,
        # то удаляем этот код, создаем новый и проверяем его.
        logger.debug("Found a repeat")
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



def get_code_group(code: str, file_path: str):
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
    assert file_path is not None and file_path != "", "File path must be str, not None"
    assert re.search(".json", file_path), "File must be in json format"

    logger.debug("Getting code gruop")
    logger.debug(f"Parameters: code={code}")

    # Получаем содержимое json файла, в котором храняться коды
    logger.debug("Retrieving data from the old file")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
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



def remove_code_file(file_path: str):
    """
    Удаляет файл с кодами

    Parameters
    ----------
    file_path: str
        Путь к файлу, который нужно удалить.
    """

    assert file_path is not None and file_path != "", "File path must be str, not None"
    assert re.search(".json", file_path), "File must be in json format"

    logger.debug(f"Removing file({file_path})")

    try:
        os.remove(file_path)
    except FileNotFoundError:
        logger.debug("File not found")
        raise FileNotFoundError("File not found")
    except Exception as e:
        logger.debug(f"Failed to remove file: {e}")
        raise Exception(e)

    logger.debug("File removed")



def get_code_file_info(file_path: str):
    """
    Возвращает информацию о файле с кодами.

    Parameters
    ----------
    file_path: str
        Путь к файлу, который нужно изучить.
    
    Return
    ------
    dict
        {
            "groups": количество групп,
            "codes": количество кодов
        }
    """

    assert file_path is not None and file_path != "", "File path must be str, not None"
    assert re.search(".json", file_path), "File must be in json format"

    logger.debug(f"Getting info from code file({file_path})")

    logger.debug("Retrieving data from the old file")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("File not found")
        raise FileNotFoundError("File not found")
    except JSONDecodeError:
        logger.error("File not supported")
        raise ValueError("File not supported")

    logger.debug("Got data from file")

    # Считаем количество групп и количество
    # кодов в полученных данных
    groups = []
    codes_count = 0
    for object in data["data"]:
        # Если название группы есть в списке уже найденных групп
        if object["group"] not in groups:
            # Если группы нет в списке найденных групп
            # Добавляем ее в этот список
            groups.append(object["group"])
        # Добавляем к числу кодов количество кодов этой группы
        codes_count += len(object["codes"])
    
    logger.debug(f"Found {len(groups)} and {codes_count} codes")

    if groups is None or codes_count == 0:
        return None
    return {"groups": len(groups), "codes": codes_count}

    

def get_codes_by_group(group: Union[str, int], file_path: str):
    """
    Возвращает коды указанной группы

    Parameters
    ----------
    group: str, int
        Группа, коды которой нужно найти

    file_path: str
        Путь к файлу, в котором будут лежать коды.

    Return
    ------
        list, None
    """
    
    assert group is not None and group != "", "Group must be str or int, not None"
    assert file_path is not None and file_path != "", "File path must be str, not None"
    assert re.search(".json", file_path), "File must be in json format"

    logger.debug("Getting codes by group")
    logger.debug(f"Parameters: group={group}")

    # Получаем содержимое json файла, в котором храняться коды
    logger.debug(f"Retrieving data from file({file_path})")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("File not found")
        raise FileNotFoundError("File not found")
    except JSONDecodeError:
        logger.error("File not supported")
        raise ValueError("File not supported")

    logger.debug("Got data from file")
    
    # Ищем коды группы в данных файла
    logger.debug("Searching codes by group")
    codes = []
    for object in data["data"]:
        if group == object["group"]:
        # Сохраняем название группы
            codes.extend(object["codes"])
            continue
    
    if len(codes) == 0:
        logger.debug(f"Group {group} not found")
        return None
    logger.debug(f"Found codes: {codes}")
    return codes

