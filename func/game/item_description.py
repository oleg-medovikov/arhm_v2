from mdls import Item

dict_ = {
    "sex": "пол",
    "speed": "скорость",
    "stealth": "скрытность",
    "strength": "сила",
    "knowledge": "знания",
    "godliness": "набожность",
    "luck": "удача",
}


def item_description(item: "Item") -> str:
    """описание предмета + требования + эффекты"""
    mess = item.description + "\n\n"

    # сначала распишем требования
    if len(item.demand):
        mess += "* Требования: *"
        for key, value in item.demand.items():
            if key == "sex":
                mess += "\n - Для мужчин" if value else "\n - Для женщин"
                continue
            mess += "\n - " + dict_.get(key, key) + "  " + str(value)
    mess += "\n\n"
    # теперь распишем эффект
    if len(item.demand):
        mess += "* Эффект: *"
        for key, value in item.effect.items():
            mess += "\n - " + dict_.get(key, key) + "  " + str(value)

    return mess
