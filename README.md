## Установка и запуск

```bash
poetry install
poetry run database
```

## Управление таблицами

Команды:

- `create_table <имя_таблицы> <столбец:тип> ...` — создать таблицу (тип: `int`, `str`, `bool`). Поле `ID:int` добавляется автоматически.
- `list_tables` — показать список таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — показать справку.
- `exit` — выйти.

Пример:

```text
database
create_table users name:str age:int is_active:bool
list_tables
drop_table users
exit
```

## Demo (asciinema)

Демонстрация работы с базовыми командами управления таблицами.

[![asciinema](https://asciinema.org/a/IfVpIfYf8Fr2FPZV.svg)](https://asciinema.org/a/IfVpIfYf8Fr2FPZV)

## CRUD-операции

Команды:

- `insert into <table> values (<v1>, <v2>, ...)` — добавить запись (ID генерируется автоматически).
- `select from <table>` — вывести все записи.
- `select from <table> where <column> = <value>` — вывести записи по условию.
- `update <table> set <column> = <new_value> where <column> = <value>` — обновить записи по условию.
- `delete from <table> where <column> = <value>` — удалить записи по условию.
- `info <table>` — информация о таблице.
- `help` — справка.
- `exit` — выход.

Пример:

```text
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
select from users where age = 28
update users set age = 29 where name = "Sergei"
delete from users where ID = 1
```

## CRUD-операции

Демонстрация работы с базой данных:

- создание таблицы
- добавление записей
- выборка данных
- обновление записей
- удаление записей

[![asciinema](https://asciinema.org/a/9imrD5Nvxc8jgIDh.png)](https://asciinema.org/a/9imrD5Nvxc8jgIDh)

## Дополнительные возможности

В проекте реализованы декораторы для повышения надёжности и удобства работы:

- **Обработка ошибок** — централизованный перехват ошибок ввода, работы с файлами и логики БД.
- **Подтверждение действий** — запрос подтверждения перед опасными операциями (удаление таблиц и записей).
- **Логирование времени выполнения** — вывод времени выполнения CRUD-операций.

## Demo (asciinema)

Демонстрация работы декораторов и основных операций базы данных:

- подтверждение удаления записей и таблиц
- обработка ошибок
- логирование времени выполнения команд

[![asciinema](https://asciinema.org/a/HwLcJEXR91UH51L5.svg)](https://asciinema.org/a/HwLcJEXR91UH51L5)
