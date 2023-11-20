from mdls import Person, Inventory, Item
from conf import MAX_BAG_CAPASITY
from func import person_change


async def item_remove(person: "Person", inventory: "Inventory", item: "Item"):
    """
    нужно проверить 2 вещи:
    есть ли пустое место в сумке, куда поместить вещь
    если у вещи есть альтернатива, ее можно снять только
    в случае наличия этой вещи в сумке
    """

    if len(inventory.bag) >= MAX_BAG_CAPASITY:
        return False, "Сумка заполнена, некуда поместить данный предмет"

    if item.alternative is not None:
        if item.alternative not in inventory.bag:
            return (
                False,
                f"Вы не можете снять {item.name}, так как у Вас нет альтернативы.",
            )

    # теперь нужно убрать эффекты предмета
    effect = {}

    for key, value in item.effect:
        effect[key] = -value

    person = await person_change(person, effect)
