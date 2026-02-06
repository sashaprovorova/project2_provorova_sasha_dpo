
ALLOWED_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns): 
  """ Создает новую таблицу и сохраняет ее структуру в метаданных """

  if "tables" not in metadata:
    metadata["tables"] = {}

  if table_name in metadata["tables"]:
    raise ValueError(f'Таблица "{table_name}" уже существует.')

  parsed_columns = [["ID", "int"]]

  for column in columns:
    if ":" not in column:
      raise ValueError(f"Некорректное значение: {column}. Попробуйте снова.")

    name, col_type = column.split(":", 1)
    name = name.strip()
    col_type = col_type.strip()

    if col_type not in ALLOWED_TYPES:
      raise ValueError(f"Некорректное значение: {col_type}. Попробуйте снова.")

    if name.lower() == "id":
      raise ValueError(f"Некорректное значение: {name}. Попробуйте снова.")

    parsed_columns.append([name, col_type])

  metadata["tables"][table_name] = {
        "columns": parsed_columns
  }

  return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata["tables"][table_name]
    return metadata