from mdls import Inventory, Item
from conf import emoji

I_def = {
    "head": "Непокрытая голова",
    "earrings": "пустые уши",
    "hands": "Пустые руки",
    "rings": "Пальцы без колец",
    "body": "Голое тело",
    "legs": "Голые ноги",
    "shoes": "Босые ноги",
    "bag": "Сумка пустая, не тянет плечо",
    "achievements": "Нет достижений",
}


async def inventory_mess(gamename: str, i_id: int, EQUIP: bool = False) -> str:
    "Генерируем сообщение для списка инвентаря"
    # нужно получить список всех предметов
    inventory = await Inventory.get(i_id)

    ITEMS = await Item.query.where(Item.id.in_(inventory.get_all())).gino.all()

    # словарь для начала, незаполненный инвентарь
    I_zero = {
        "head": "",
        "earrings": "",
        "hands": "",
        "rings": "",
        "body": "",
        "legs": "",
        "shoes": "",
        "bag": "",
        "achievements": "",
    }

    for key, value in ITEMS.items():
        if isinstance(value, list):
            continue
        for item in value:
            I_zero[key] = " " + emoji(item["emoji"]) + " " + item.name

    for key, value in I_zero.items():
        if len(value) < 2:
            I_zero[key] = I_def[key]

    LIST = (
        f"*Ваш инвентарь* {PERS.gamename}\n",
        f"\n*Голова:* {I_zero['head']}",
        f"\n*Уши:* {I_zero['earrings']}",
        f"\n*В руках:* {I_zero['hands']}",
        f"\n*Кольца:* {I_zero['rings']}",
        f"\n*На теле:* {I_zero['body']}",
        f"\n*Ноги:* {I_zero['legs']}",
        f"\n*Обувь:* {I_zero['shoes']}",
        f"\n*Достижения:* {I_zero['achievements']}",
        "\n\nВаш персонаж сейчас использует" if EQUIP else "\n\nВ вашей сумке:",
    )

    return "".join(str(x) for x in LIST)
