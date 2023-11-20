from mdls import Person, Item, Inventory
from func.game.demand import demand
from func.game.person_change import person_change
from conf import MAX_RINGS_EQUIP

equip_slots = [
    "head",
    "neck",
    "earrings",
    "onehand",
    "twohands",
    "rings",
    "body",
    "legs",
    "shoes",
]


async def item_using(
    person: "Person", inventory: "Inventory", item: "Item"
) -> tuple[bool, str]:
    """ """
    # нужно проверить требования к персонажу, перед использованием
    if not await demand(person, item.demand):
        # если не прошел проверку, то просто возвращаем сообщение
        return False, item.mess_equip_fail

    # если премет надевается, нужно проверить наличие слота!
    # если надетый предмет имеет альтернативу
    # тут это не проверяется!
    # проверки наличия пустого слота достаточна!
    empty_slot = False
    if item.slot in ["head", "neck", "earrings", "body", "legs", "shoes"]:
        if getattr(inventory, item.slot) is None:
            empty_slot = True
    if item.slot == "onehand":
        # если занято меньше 2 рук
        if len(inventory.hands) < 2:
            empty_slot = True
    if item.slot == "twohands":
        if len(inventory.hands) == 0:
            empty_slot = True
    if item.slot == "rings":
        if len(inventory.rings) < MAX_RINGS_EQUIP:
            empty_slot = True
    if item.slot == "bag":
        empty_slot = True

    if not empty_slot:
        return False, "нет доступного слота, снимите что-то с персонажа"

    # теперь применяем изменения характеристик персонажа
    person = await person_change(person, item.effect)

    # предмет нужно удалить из сумки
    inventory.bag.remove(item.id)
    dict_ = {"bag": inventory.bag}
    await inventory.update(**dict_).apply()

    # если он не одноразовый засунуть его в слот
    if not item.single_use:
        if item.slot in ["head", "neck", "earrings", "body", "legs", "shoes"]:
            dict_ = {item.slot: item.id}
        if item.slot == "onehand":
            dict_ = {"hands": inventory.hands.append(item.id)}
        if item.slot == "twohands":
            dict_ = {"hands": [item.id, item.id]}
        if item.slot == "rings":
            dict_ = {"rings": inventory.rings.append(item.id)}
        if item.slot == "bag":
            dict_ = {"bag": inventory.bag.append(item.id)}

        await inventory.update(**dict_).apply()

    return True, item.mess_equip
