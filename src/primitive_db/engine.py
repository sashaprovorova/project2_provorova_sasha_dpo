import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from src.primitive_db.decorators import create_cacher
from src.primitive_db.parser import parse_set, parse_where
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

select_cache = create_cacher()

META_FILE = "db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print('<command> insert into <имя_таблицы> values (<значение1>,'
    ' <значение2>, ...) - создать запись.')
    print('<command> select from <имя_таблицы> where <столбец> = <значение> -' \
    ' прочитать записи по условию.')
    print('<command> select from <имя_таблицы> - прочитать все записи.')
    print('<command> update <имя_таблицы> set <столбец> = <новое_значение> ' \
    'where <столбец> = <значение> - обновить запись.')
    print('<command> delete from <имя_таблицы> where <столбец> = <значение> - ' \
    'удалить запись.')
    print('<command> info <имя_таблицы> - вывести информацию о таблице.')
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """ Запускает основной цикл работы базы данных """
    print_help()

    while True:
        metadata = load_metadata(META_FILE)

        user_input = prompt.string("Введите команду: ").strip()
        if not user_input:
            continue

        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Некорректное значение: команда. Попробуйте снова.")
            continue

        command = args[0]
        rest = args[1:]
        if command == "exit":
            return

        elif command == "help":
            print_help()

        elif command == "list_tables":
            tables = metadata.get("tables", {})
            if not tables:
                print("Таблиц нет")
            else:
                for table_name in tables.keys():
                    print(f"- {table_name}")

        elif command == "create_table":
            if len(rest) < 2:
                print("Некорректное значение: create_table. Попробуйте снова.")
                continue

            table_name = rest[0]
            columns = rest[1:]

            try:
                metadata = create_table(metadata, table_name, columns)
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            save_metadata(META_FILE, metadata)
            select_cache.clear()
            cols = metadata["tables"][table_name]["columns"]
            cols_str = ", ".join([f"{name}:{col_type}" for name, col_type in cols])
            print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')

        elif command == "drop_table":
            if len(rest) != 1:
                print("Некорректное значение: drop_table. Попробуйте снова.")
                continue

            table_name = rest[0]

            try:
                metadata = drop_table(metadata, table_name)
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            save_metadata(META_FILE, metadata)
            select_cache.clear()
            print(f'Таблица "{table_name}" успешно удалена.')
        elif command == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print("Некорректное значение: insert. Попробуйте снова.")
                continue

            table_name = args[2]
            values_token = " ".join(args[4:]).strip()

            if not (values_token.startswith("(") and values_token.endswith(")")):
                print("Некорректное значение: values. Попробуйте снова.")
                continue

            inside = values_token[1:-1].strip()
            raw_values = [val.strip() for val in inside.split(",")]

            fixed_values = []
            for val in raw_values:
                low = val.lower()
                if low in {"true", "false"}:
                    fixed_values.append(low)  
                elif val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    fixed_values.append(val)    
                else:
    
                    fixed_values.append(f'"{val}"')

            try:
                values = [parse_where(f"x = {val}")["x"] for val in fixed_values]
            except ValueError as error:
                print(error)
                continue

            table_data = load_table_data(table_name)
            try:
                table_data = insert(metadata, table_name, table_data, values)
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            save_table_data(table_name, table_data)
            select_cache.clear()
            record_id = table_data[-1]["ID"]
            message = (
                f'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".'
            )
            print(message)

        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print("Некорректное значение: select. Попробуйте снова.")
                continue

            table_name = args[2]
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            table_data = load_table_data(table_name)

            where_clause = None
            if len(args) > 3:
                if len(args) >= 5 and args[3] == "where":
                    cond_text = " ".join(args[4:])
                    try:
                        where_clause = parse_where(cond_text)
                    except ValueError as error:
                        print(error)
                        continue
                else:
                    print(f"Функции {command} нет. Попробуйте снова.")
                    continue

            where_key = (
                tuple(sorted(where_clause.items()))
                if where_clause
                else None
            )
            cache_key = (table_name, where_key)

            result = select_cache(
                cache_key,
                lambda: select(table_data, where_clause),
            )

            schema = metadata["tables"][table_name]["columns"]
            headers = [name for name, _column_type in schema]

            table = PrettyTable()
            table.field_names = headers
            for row in result:
                table.add_row([row.get(header) for header in headers])

            print(table)

        elif command == "update":
            if "set" not in args or "where" not in args or len(args) < 6:
                print("Некорректное значение: update. Попробуйте снова.")
                continue

            table_name = args[1]
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_idx = args.index("set")
            where_idx = args.index("where")

            set_text = " ".join(args[set_idx + 1:where_idx])
            where_text = " ".join(args[where_idx + 1:])

            if "=" in set_text:
                left, right = set_text.split("=", 1)
                right = right.strip()
                low = right.lower()
                if not (
                    (right.startswith('"') and right.endswith('"')) or
                    (right.startswith("'") and right.endswith("'")) or
                    low in {"true", "false"} or
                    right.isdigit() or (right.startswith("-") and right[1:].isdigit())
                ):
                    set_text = f'{left.strip()} = "{right}"'

                if "=" in where_text:
                    left, right = where_text.split("=", 1)
                    right = right.strip()
                    low = right.lower()
                    is_negative_int = right.startswith("-") and right[1:].isdigit()
                    is_int = right.isdigit() or is_negative_int
                    if "=" in where_text:
                        left, right = where_text.split("=", 1)
                        right = right.strip()
                        low = right.lower()

                        is_quoted = (
                            (right.startswith('"') and right.endswith('"'))
                            or (right.startswith("'") and right.endswith("'"))
                        )
                        is_bool = low in {"true", "false"}
                        
                        is_negative_int = right.startswith("-") and right[1:].isdigit()
                        is_int = right.isdigit() or is_negative_int

                        if not (is_quoted or is_bool or is_int):
                            where_text = f'{left.strip()} = "{right}"'

                try:
                    set_clause = parse_set(set_text)
                    where_clause = parse_where(where_text)
                except ValueError as error:
                    print(error)
                    continue

            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)
            select_cache.clear()
            updated_rows = select(table_data, where_clause)
            if updated_rows:
                record_id = updated_rows[0]["ID"]
                message = (
                    f'Запись с ID={record_id} в таблице "{table_name}" '
                    "успешно обновлена."
                )
                print(message)
            else:
                print("Нет подходящих записей для обновления.")

        elif command == "delete":
            if len(args) < 6 or args[1] != "from" or args[3] != "where":
                print("Некорректное значение: delete. Попробуйте снова.")
                continue

            table_name = args[2]
            if "tables" not in metadata or table_name not in metadata["tables"]:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_text = " ".join(args[4:])
            try:
                where_clause = parse_where(where_text)
            except ValueError as error:
                print(error)
                continue

            table_data = load_table_data(table_name)

            to_delete = select(table_data, where_clause)
            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)
            select_cache.clear()

            if to_delete:
                record_id = to_delete[0]["ID"]
                message = (
                    f'Запись с ID={record_id} успешно удалена из таблицы '
                    f'"{table_name}".'
                )
                print(message)
            else:
                print("Нет подходящих записей для удаления.")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")

    

