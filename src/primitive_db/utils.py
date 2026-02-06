import json
from pathlib import Path
from typing import Any

def load_metadata(filepath):
    """ Загружает данные из JSON-файла """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_metadata(filepath, data):
    """ Сохраняет переданные данные в JSON-файл """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)