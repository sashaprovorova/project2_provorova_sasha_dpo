import time

import prompt


def handle_db_errors(func):
    """ Централизованно обрабатывает ошибки операций БД """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print( "Ошибка: файл не найден")
        except KeyError as error:
            print(f"Ошибка: таблица или столбец {error} не найдены.")
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except Exception as error:
            print(f"Неизвестная ошибка: {error}")

    return wrapper

def confirm_action(action_name):
    """ Запрашивает подтверждение пользователя перед опасной операцией """

    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = prompt.string(
              f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if answer.lower() != "y":
              print("Операция отменена.")
              return args[0] if args else None
            return func(*args, **kwargs)

        return wrapper

    return decorator

def log_time(func):
    """ Замеряет и выводит время выполнения функции """

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()

        elapsed = end_time - start_time
        print(
            f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд."
        )
        return result

    return wrapper


def create_cacher():
    """ Возвращает функцию, которая кэширует результат по ключу """
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result
    
    def clear():
        cache.clear()

    cache_result.clear = clear

    return cache_result