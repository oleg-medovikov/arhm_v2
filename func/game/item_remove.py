from sqlalchemy import and_

from mdls import Person, Inventory, Item
from conf import MAX_BAG_CAPASITY
from func.game.person_change import person_change
from func.game.demand import demand


async def item_remove(
    person: "Person", inventory: "Inventory", item: "Item"
) -> tuple[bool, str, dict]:
    """
    нужно проверить 2 вещи:
    есть ли пустое место в сумке, куда поместить вещь
    если у вещи есть альтернатива, ее можно снять только
    в случае наличия этой вещи в сумке
    Необходимо проверить наличие, этой вещи, что она подходит по требованиям,
    предложить выбор, если их несколько
    и сразу после remove запустить using
    чтобы случилось переодевание
    """

    if len(inventory.bag) >= MAX_BAG_CAPASITY:
        return False, "Сумка заполнена, некуда поместить данный предмет", {}

    if item.alternative is not None:
        # если alternative -1 - подойтет любой предмет в этот слот
        # если конкретное число - только предмет с таким id
        if item.alternative > 0 and item.alternative not in inventory.bag:
            return False, item.mess_remove_fail, {}
        # необходимо вытащить предметы из базы, чтобы узнать их слоты
        alter_items = await Item.query.where(
            and_(Item.id.in_(inventory.bag), Item.slot == item.slot)
        ).gino.all()
        # необходимо проверить требования
        _alter_items_ = []
        for _ in alter_items:
            if await demand(person, _.demand):
                _alter_items_.append(_)
        # формируем словарь для кнопочек выбора из подходящих вещей
        dict_ = {}
        for _ in _alter_items_:
            dict_[_.id] = _.name
        if len(dict_):
            # тут мы должны снять предмет, а для начала снять эффект
            effect = {}

            for key, value in item.effect:
                effect[key] = -value

            person = await person_change(person, effect)
            # теперь удаляем из слота и кидаем в сумку
            inventory.bag.append(item.id)
            if item.slot in ["head", "neck", "earrings", "body", "legs", "shoes"]:
                inv_ = {item.slot: None, "bag": inventory.bag}
            if item.slot == "onehand":
                inventory.hands.remove(item.id)
                inv_ = {"hands": inventory.hands, "bag": inventory.bag}
            if item.slot == "twohands":
                inv_ = {"hands": [], "bag": inventory.bag}
            if item.slot == "rings":
                inventory.rings.remove(item.id)
                inv_ = {"rings": inventory.rings, "bag": inventory.bag}

            await inventory.update(**inv_).apply()
            return True, item.mess_remove, dict_
        else:
            return False, item.mess_remove_fail, {}

    # тут разбираем предметы, для которых не нужна альтернатива
    # теперь нужно убрать эффекты предмета
    effect = {}

    for key, value in item.effect:
        effect[key] = -value

    person = await person_change(person, effect)

    # теперь удаляем из слота и кидаем в сумку
    inventory.bag.append(item.id)
    if item.slot in ["head", "neck", "earrings", "body", "legs", "shoes"]:
        inv_ = {item.slot: None, "bag": inventory.bag}
    if item.slot == "onehand":
        inventory.hands.remove(item.id)
        inv_ = {"hands": inventory.hands, "bag": inventory.bag}
    if item.slot == "twohands":
        inv_ = {"hands": [], "bag": inventory.bag}
    if item.slot == "rings":
        inventory.rings.remove(item.id)
        inv_ = {"rings": inventory.rings, "bag": inventory.bag}

    await inventory.update(**inv_).apply()

    return True, item.mess_remove, {}
