from mdls import Person


L_STANDART = [
    "speed",
    "stealth",
    "strength",
    "knowledge",
    "godliness",
    "luck",
    "experience",
    "bless",
    "proof",
    "money",
    "health",
    "mind",
    "health_max",
    "mind_min",
]
L_POSITIVE = ["hunger", "weary"]
L_ID = ["location"]
L_BOOL = ["death"]


async def person_change(person: "Person", DICT: dict, negative=False) -> "Person":
    """
    Изменение параметров персонажа
    """
    updates = {}
    for key, value in DICT.items():
        try:
            old = getattr(person, key)
        except AttributeError:
            continue

        if negative and isinstance(value, int):
            value = -value

        itog = {
            # стандартно складываем значения
            key in L_STANDART: old + value,
            # не опускаем ниже нуля
            key in L_POSITIVE: old + value if old + value > 0 else 0,
            # заменяем значение
            key in L_ID: value,
            # отдельно для bool
            key in L_BOOL: bool(value),
        }.get(True, old)

        # все имзенения засовываем в словарь
        updates[key] = itog

    # применяем изменения в базе
    if len(updates):
        # с путым словарем нельзя
        person = await person.update(**updates).apply()
    return person
