from mdls import Person, Inventory, PersonDefault, Item
from func.game.item_using import item_using


def _get_value(MIN: int, MAX: int, DICE: int) -> int:
    return MIN + int(DICE * (MAX - MIN) / 6)


async def person_create(user_data: dict) -> "Person":
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

    health = _get_value(default.health_min, default.health_max, dice)
    mind = _get_value(default.mind_min, default.mind_max, dice)

    person = await Person.create(
        u_id=user_data.get("user_id"),
        loc_id=default.start_loc_id,
        i_id=inventory.id,
        gamename=user_data.get("gamename"),
        sex=user_data.get("sex"),
        profession=user_data.get("profession"),
        money=_get_value(default.money_min, default.money_max, dice),
        health_max=health,
        health=health,
        mind_max=mind,
        mind=mind,
        speed=_get_value(default.speed_min, default.speed_max, dice),
        stealth=_get_value(default.stealth_min, default.stealth_max, dice),
        strength=_get_value(default.strength_min, default.strength_max, dice),
        knowledge=_get_value(default.knowledge_min, default.knowledge_max, dice),
        godliness=_get_value(default.godliness_min, default.godliness_max, dice),
        luck=_get_value(default.luck_min, default.luck_max, dice),
    )

    # надеваем стартовые предметы
    for _ in default.start_items:
        item = await Item.get(_)
        if item.slot == "bag":
            continue
        person = await Person.get(person.id)
        inventory = await Inventory.get(inventory.id)
        await item_using(person, inventory, item)

    return person
