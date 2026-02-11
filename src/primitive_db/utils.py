import json
from pathlib import Path


def load_metadata(filepath):
    """ Загружает данные из JSON-файла """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def load_table_data(table_name): 
    """ Загружает данные таблицы из JSON-файла. """
    filepath = Path("data") / f"{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data =  json.load(file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_metadata(filepath, data):
    """ Сохраняет переданные данные в JSON-файл """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл."""
    filepath = Path("data") / f"{table_name}.json"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)