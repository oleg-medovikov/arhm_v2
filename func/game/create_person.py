from mdls import Person, Inventory, PersonDefault


def _get_value(MIN: int, MAX: int, DICE: int) -> int:
    return MIN + int(DICE * (MAX - MIN) / 6)


async def create_person(user_data: dict) -> "Person":
    """"""
    dice = user_data.get("dice", 1)
    # достаем значения по умолчанию
    default = await PersonDefault.get(user_data.get("profession"))
    # создаем новый инвентарь
    inventory = await Inventory.create(
        hands=[],
        rings=[],
        bag=default.start_items,
    )

    person = await Person.create(
        u_id=user_data.get("user_id"),
        loc_id=default.start_loc_id,
        i_id=inventory.id,
        gamename=user_data.get("gamename"),
        sex=user_data.get("sex"),
        profession=user_data.get("profession"),
        gametime=1,
        stage=1,
        money=_get_value(default.money_min, default.money_max, dice),
    )

    return person
