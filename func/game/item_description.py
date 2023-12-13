from mdls import Item

dict_ = {
    "sex": "пол",
    "speed": "скорость",
    "stealth": "скрытность",
    "strength": "сила",
    "knowledge": "знания",
    "godliness": "набожность",
    "luck": "удача",
    "mind_max": "максимум рассудка",
    "health_max": "максимум здоровья",
    "positive": "",
    "negative": "",
}


def item_description(item: "Item") -> str:
    """описание предмета + требования + эффекты"""
    mess = item.description

    # сначала распишем требования
    if len(item.demand):
        mess += "\n\n * Требования: *"
        for key, value in item.demand.items():
            if key == "sex":
                mess += "\n - Для мужчин" if value else "\n - Для женщин"
                continue
            mess += "\n - " + dict_.get(key, key) + "  " + str(value)
    # теперь распишем эффект
    if len(item.effect):
        mess += "\n\n * Эффект: *"
        for key, value in item.effect.items():
            if key in ["positive", "negative"]:
                mess += "\n - " + str(value)
                continue
            mess += "\n - " + dict_.get(key, key) + "  " + str(value)

    return mess
