import shlex

import prompt

from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import load_metadata, save_metadata

META_FILE = "db_meta.json"

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
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
            print(f'Таблица "{table_name}" успешно удалена.')

        else:
            print(f"Функции {command} нет. Попробуйте снова.")

    

