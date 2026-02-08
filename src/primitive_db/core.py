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
    """ Удаляет таблицу из метаданных """
    
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata["tables"][table_name]
    return metadata

def insert(metadata, table_name, table_data, values):
  """ Добавляет запись и возвращает обновлённые данные таблицы """
    
  if "tables" not in metadata or table_name not in metadata["tables"]:
    raise ValueError(f'Таблица "{table_name}" не существует.')

  schema = metadata["tables"][table_name]["columns"] 
  expected_values = len(schema) - 1 
  if len(values) != expected_values:
    raise ValueError("Некорректное значение: количество values. Попробуйте снова.")

  record = {}

  new_id = 1
  if table_data:
    ids = [row.get("ID", 0) for row in table_data]
    new_id = max(ids) + 1
  record["ID"] = new_id

  for (col_name, col_type), raw_val in zip(schema[1:], values):
    if col_type not in ALLOWED_TYPES:
      raise ValueError(f"Некорректное значение: {col_type}. Попробуйте снова.")

    if col_type == "int":
      if isinstance(raw_val, bool):
        raise ValueError(f"Некорректное значение: {raw_val}. Попробуйте снова.")
      try:
        record[col_name] = int(raw_val)
      except (TypeError, ValueError):
        raise ValueError(f"Некорректное значение: {raw_val}. Попробуйте снова.")

    elif col_type == "bool":
      if isinstance(raw_val, bool):
        record[col_name] = raw_val
      elif isinstance(raw_val, str):
        val = raw_val.strip().lower()
        if val == "true":
          record[col_name] = True
        elif val == "false":
          record[col_name] = False
        else:
          raise ValueError(f"Некорректное значение: {raw_val}. Попробуйте снова.")
      else:
        raise ValueError(f"Некорректное значение: {raw_val}. Попробуйте снова.")

    elif col_type == "str":
      if not isinstance(raw_val, str):
        raise ValueError(f"Некорректное значение: {raw_val}. Попробуйте снова.")
      record[col_name] = raw_val
    
  
  table_data.append(record)
  return table_data


def select(table_data, where_clause=None):
  """ Возвращает все записи или записи по условию. """
  if where_clause is None:
    return table_data

  if len(where_clause) != 1:
    raise ValueError("Некорректное значение: where. Попробуйте снова.")

  key, val = next(iter(where_clause.items()))
  return [row for row in table_data if row.get(key) == val]


def update(table_data, set_clause, where_clause):
  """ Обновляет записи по условию и возвращает обновлённые данные """
  if not set_clause or len(set_clause) != 1:
    raise ValueError("Некорректное значение: set. Попробуйте снова.")
  if not where_clause or len(where_clause) != 1:
    raise ValueError("Некорректное значение: where. Попробуйте снова.")

  where_key, where_val = next(iter(where_clause.items()))
  set_key, set_val = next(iter(set_clause.items()))

  for row in table_data:
    if row.get(where_key) == where_val:
      row[set_key] = set_val

  return table_data

def delete(table_data, where_clause):
  """ Удаляет записи по условию и возвращает обновлённые данные """
  if not where_clause or len(where_clause) != 1:
    raise ValueError("Некорректное значение: where. Попробуйте снова.")

  where_key, where_val = next(iter(where_clause.items()))
  return [row for row in table_data if row.get(where_key) != where_val]