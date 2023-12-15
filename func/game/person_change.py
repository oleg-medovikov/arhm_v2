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
]
L_POSITIVE = ["hunger", "weary"]
L_ID = ["location"]
L_BOOL = ["death"]


async def person_change(person: Person, DICT: dict, negative=False) -> "Person":
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

        # отдельная логика для изменения максимума здоровья и рассудка
        # рассудок и здоровье меняется в относительных значениях от предыдущего значения
        # формула: x2 = x1*(old + value)/old с обычным округлением до целого
        if key in ["health_max", "mind_max"]:
            key_x = key.replace("_max", "")
            x1 = getattr(person, key_x)
            up = {
                key: old + value,
                key_x: int(round(x1 * (old + value) / old)),
            }
            person = await person.update(**up).apply()
            continue
        # отдельная логика для изменения здоровья и рассудка
        # они не могут быть больше максимума
        if key in ["health", "mind"]:
            x_max = getattr(person, key + "_max")
            up = {key: old + value if old + value <= x_max else x_max}
            person = await person.update(**up).apply()
            continue

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
