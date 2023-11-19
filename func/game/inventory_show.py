from mdls import Inventory, Item
from conf import emoji

I_def = {
    "head": "непокрытая голова",
    "earrings": "чистые уши",
    "neck": "открытая шея",
    "hands": "пустые руки",
    "rings": "пальцы без колец",
    "body": "голое тело",
    "legs": "голые ноги",
    "shoes": "босые ноги",
}


async def inventory_show(i_id: int, EQUIP: bool = False) -> tuple[str, dict]:
    """
    Генерируем текст сообщения для инвентаря
    если EQUIP под сообщением будет свисок одетых предметов
    иначе снизу будет содержимое сумки
    """
    # нужно получить список всех предметов
    inventory = await Inventory.get(i_id)
    ITEMS = await Item.query.where(Item.id.in_(inventory.get_all())).gino.all()
    ITEM_DICT = {}
    for item in ITEMS:
        ITEM_DICT[item.id] = item

    # если атрибут инвенторя содержит номер айтема в I_def меняем value соответсвующего атрибута
    for attr in ["head", "earrings", "neck", "body", "legs", "shoes"]:
        if getattr(inventory, attr) is not None:
            item = ITEM_DICT[getattr(inventory, attr)]
            I_def[attr] = " " + emoji(item.emoji) + " " + item.name
    # тоже для списков
    for attr in ["hands", "rings"]:
        if len(getattr(inventory, attr)):
            I_def[attr] = ""
            for _ in getattr(inventory, attr):
                item = ITEM_DICT[getattr(inventory, attr)]
                I_def[attr] += " " + emoji(item.emoji) + " " + item.name

    # формируем список предметов для кнопочек под сообщением
    if EQUIP:
        numbers = inventory.get_equip()
    else:
        numbers = inventory.bag
    DICT = {}
    for _ in numbers:
        DICT[_] = ITEM_DICT[_].name
    # формируем сообщение
    LIST = (
        "*Ваш инвентарь* \n",
        f"\n*Голова:* {I_def['head']}",
        f"\n*Уши:* {I_def['earrings']}",
        f"\n*Шея:* {I_def['neck']}",
        f"\n*В руках:* {I_def['hands']}",
        f"\n*Кольца:* {I_def['rings']}",
        f"\n*На теле:* {I_def['body']}",
        f"\n*Ноги:* {I_def['legs']}",
        f"\n*Обувь:* {I_def['shoes']}",
        "\n\nВаш персонаж сейчас использует" if EQUIP else "\n\nВ вашей сумке:",
    )

    return "".join(str(x) for x in LIST), DICT
