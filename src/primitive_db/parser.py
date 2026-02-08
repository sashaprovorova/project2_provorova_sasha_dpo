def _parse_value(raw):
    raw = raw.strip()

    is_double = raw.startswith('"') and raw.endswith('"')
    is_single = raw.startswith("'") and raw.endswith("'")
    if is_double or is_single:
        return raw[1:-1]

    low = raw.lower()
    if low == "true":
        return True
    if low == "false":
        return False

    if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
        return int(raw)

    raise ValueError(f"Некорректное значение: {raw}. Попробуйте снова.")


def parse_where(text):
    """ Разбирает where-условие вида 'age = 28' """
    if "=" not in text:
        raise ValueError(f"Некорректное значение: {text}. Попробуйте снова.")
    left, right = text.split("=", 1)
    column = left.strip()
    value = _parse_value(right.strip())
    return {column: value}


def parse_set(text):
    """ Разбирает set-условие вида 'age = 29' """
    if "=" not in text:
        raise ValueError(f"Некорректное значение: {text}. Попробуйте снова.")
    left, right = text.split("=", 1)
    column = left.strip()
    value = _parse_value(right.strip())
    return {column: value}