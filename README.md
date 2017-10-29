# pro_group
Виволікає ціни і записую їх у файл і/або базу даних, далі БД.
Пари знаходяться у файлі **run.py** глобальна змінна - кортеж `PAIRS`. 

## Requirements
- Python >=3
- requests==2.7.3.2
- psycopg2==2.18.4
- Ubuntu 16.04

## Install
- `sudo apt-get install python3-pip`
- `sudo apt-get install python-psycopg2`


Для роботи портібно встановити реляційну БД postgresql,
налаштування параметрів БД необхідно змінити у файлі `config.py`.

Створюємо virtualenv (якщо немає `sudo pip3 install virtualenv`) `virtualenv -p python3 .venv` та активовуємо `source .venv/bin/activate`. Після цього встановлюємо все необхідне `pip3 install -r requirements.txt`

## Run
Запуск здійснюється за допомогою файлу **run.py**, `python3 run.py [options]`

**Options:**

-f **filename**
--filename **filename**
    Ім'я файлу куди зберігати таблицю, e.g. *.csv;
    
-d
--database
    Зберігати таблицю в БД, за замовчуванням ні.
    
## Example
- `python3 run.py -h`
- `python3 run.py`
- `python3 run.py -f data.csv`
- `python3 run.py -f data.csv -d`
