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

Запись терминальной сессии: `demo.cast`

Просмотр локально:

```bash
asciinema play demo.cast
```
