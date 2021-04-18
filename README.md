# PromoCodeAdmin
Приложение генерирующее промокоды.

<details open="open">
  <summary>Разделы</summary>
  <ol>
    <li>
      <a href="#задача">Задача</a>
    </li>
    <li>
      <a href="#требования">Требования</a>
    </li>
    <li>
      <a href="#настройка-перед-использованием">Настройка перед использованием</a>
      <ul>
        <li><a href="#установка-приложения">Установка приложения</a></li>
        <li><a href="#настройка">Настркойка</a></li>
      </ul>
    </li>
    <li>
      <a href="#использование">Испльзование</a>
      <ul>
        <li><a href="#генерация-новых-промо-кодов">Генерация новых промо кодов</a></li>
        <li><a href="#получение-группы-по-указанному-промо-коду">Получение группы по указанному промо коду</a></li>
        <li><a href="#получение-информации-о-файле-с-промо-кодами">Получение информации о файле с промо кодами</a></li>
        <li><a href="#получение-промо-кодов-по-указанной-группе">Получение промо кодов по указанной группе</a></li>
        <li><a href="#удаление-файла-с-промо-кодами">Удаление файла с промо кодами</a></li>
      </ul>
    </li>
    <li>
      <a href="#тесты">Тесты</a>
    </li>
  </ol>
</details>


## Задача
Написать генератор промо кодов и их проверку с помощью Django. Команда должна генерировать коды по выделенным группам, группой может быть номер или строка и сохранять результат в json файл из которого потом можно будет проверить код. Код должен быть уникальным из любого набора символов.

## Требования
- Создать команду, которая будет принимать два аргумента: `amount`, `group`. Результатом выполнения должен стать json файл в котором будут коды сгруппированы по группам.
- Промо код должен быть **уникальным** и **не повторяться** в остальных уже созданных группах.
- Файл с кодами **не должен перезаписываться**, а должен **добавлять в существующий** файл новые коды и группы.


## Настройка перед использованием

Для запуска приложения, у вас должен быть установлен python,

### Установка приложения

1. Перейдите в директорию, куда хотите установить приложение:
  ```
  cd ПУТЬ К ФАЙЛУ
  ```
2. Скачайте или клонируйте репозиторий:
  ```
  git clone https://github.com/who-man-tech/PromoCodeAdmin.git
  ```

### Настройка
1. Перейдите в папку с приложением:
  cd PromoCodeAdmin
2. Установите все пакеты:
  ```
  pip install -r requirements.txt
  ```


## Использование
Чтобы получить доступ к командам необходимо перейти в директорию [`app/`](app/):
  ```
  cd app
  ```

Для запуска любой команды приложения, необходимо вводить следующую последовательность:
  ```
  python manage.py КОМАНДА
  ```
где `КОМАНДА` - одна из команд приведенных ниже.


### Генерация новых промо кодов

Команда, которая генерирует новые уникальные промо кодыи сохраняет их в файл.
В консоле будут указаны новые промокоды.

#### Команда

  ```
  gen_codes -a КОЛИЧЕСТВО ПРОМО КОДОВ -g НАЗВАНИЕ ГРУППЫ -p ПУТЬ К ФАЙЛУ -r ФЛАГ ПЕРЕСОДАНИЯ ФАЙЛА
  ```

#### Параметры команды

- `-a` или `--amount` - количество промо кодов(число).
- `-g` или `--group` - название группы создаваемых промо кодов(строка или число).
- `-p` или `--path` - путь к файлу, в котором будут храниться промо коды. Должен быть указан файл в формате json(строка).
- `-r` или `--recreate` - если этот параметр указан, то перед созданием новых промо кодов, содержимое файла очиститься.

#### Пример

  ```
  python manage.py gen_codes -a 10 -g "avtostop" -p "data/codes.json" -r
  ```


### Получение группы по указанному промо коду

Команда, которая выводит название группы, которой принадлежит код.

#### Команда

  ```
  get_code_group -c ПРОМО КОД -p ПУТЬ К ФАЙЛУ
  ```

#### Параметры команды:

- `-с` или `--code` - промо код, группу которого нужно найти(строка).
- `-p` или `--path` - путь к файлу, в котором находятся промо коды. Должен быть указан файл в формате json(строка).

#### Пример

  ```
  python manage.py get_code_group -c "UirmGt" -p "data/codes.json"
  ```


### Получение информации о файле с промо кодами

Команда, которая выводит количество групп и кодов в файле с промо кодами.

#### Команда

  ```
  get_file_info -p ПУТЬ К ФАЙЛУ
  ```

#### Параметры команды

- `-p` или `--path` - путь к файлу, в котором будут искаться промо код и его группа. Должен быть указан файл в формате json(строка).

#### Пример

  ```
  python manage.py get_file_info -p "data/codes.json"
  ```


### Получение промо кодов по указанной группе

Команда, которая выводит промо коды указанной группы.

#### Команда

  ```
  get_group_codes -g НАЗВАНИЕ ГРУППЫ -p ПУТЬ К ФАЙЛУ
  ```

#### Параметры команды

- `-g` или `--group` - название группы, коды которой нужно вывести(строка или число).
- `-p` или `--path` - путь к файлу, в котором будут искаться промо код и его группа. Должен быть указан файл в формате json(строка).

#### Пример

  ```
  python manage.py get_group_codes -g "avtostop" -p "data/codes.json"
  ```


### Удаление файла с промо кодами

Команда, которая удаляет указанный файл с промо кодами.

#### Команда

  ```
  rm_file -p ПУТЬ К ФАЙЛУ
  ```

#### Параметры команды

- `-p` или `--path` - путь к файлу, который нужно удалить. Должен быть указан файл в формате json(строка).

#### Пример

  ```
  python manage.py rm_file -p "data/codes.json"
  ```


## Тесты
Все тесты находятся в директории [`app/promo_code/tests/`](app/promo_code/tests/)
  ```
  cd app/promo_code/tests/
  ```

#### Запуск тестов
Для запуска тестов необходимо ввести следующую команду:
  ```
  python manage.py test promo_code.tests
  ```

### Реализованные тесты
- Проверка выполнения команды генерации новых промо кодов(`gen_codes`).
- Проверка выполнения команды нахождения группы по указанному коду(`get_code_group`).