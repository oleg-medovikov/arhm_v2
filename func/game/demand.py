from datetime import datetime, timedelta

from mdls import Person, Inventory


LIST_STAT = [
    "money",
    "health",
    "mind",
    "speed",
    "stealth",
    "strength",
    "knowledge",
    "godliness",
    "luck",
    "hunger",
    "weary",
]

LIST_PERS = ["sex", "profession"]


async def demand(person: "Person", DEMAND: dict) -> bool:
    "Прохождение проверки персонажем"
    for key, value in DEMAND.items():
        CHECK = {
            key in LIST_PERS: _check_pers_str(person, key, value),
            key == "location": _check_location(person.loc_id, value),
            key in LIST_STAT: _check_stat(person, key, value),
            key == "time": _time_cheack(person.gametime, value),
            key == "less_money": _less_money(person.money, value),
            key == "item": _check_item(person.i_id, value, True),
            key == "not_item": _check_item(person.i_id, value, False),
        }.get(True)

        if CHECK is None:
            "несуществующая проверка  - пропускаем"
            continue
        if not await CHECK:
            "если провалена хоть одна проверка, незачем проверять далее"
            return False
    return True


async def _check_item(i_id: int, item: int, have: bool) -> bool:
    "нужно достать все предметы инвентаря и проверить есть в нем такой предмет или нет"
    inventory = await Inventory.get(i_id)
    all_items = inventory.get_all()

    if have:
        return item in all_items
    else:
        return item not in all_items


async def _check_pers_str(person: "Person", key: str, value: int) -> bool:
    return getattr(person, key) == value


async def _check_location(location: int, value: int) -> bool:
    "тут значение должно совпадать, а не больше или равно"
    return location == value


async def _less_money(stat: int, value: int) -> bool:
    "проверка что денег мало, меньше, чем значение"
    return stat < value


async def _time_cheack(gametime: int, VALUE: str) -> bool:
    TIME = datetime.strptime("09:00", "%H:%M") + timedelta(minutes=15 * gametime)

    STRING = {
        TIME.hour in range(0, 6): "ночь",
        TIME.hour in range(6, 9): "утро",
        TIME.hour in range(9, 19): "день",
        TIME.hour in range(19, 24): "вечер",
    }.get(True, "")
    return STRING == VALUE


async def _check_stat(person: "Person", key: str, value: int) -> bool:
    "числовые проверки"
    INT = getattr(person, key)
    return abs(INT) > abs(value) and INT * value > 0
