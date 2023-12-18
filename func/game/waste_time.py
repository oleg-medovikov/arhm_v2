from datetime import datetime

from mdls import Person
from conf import MAX_HUNGER, MAX_WEARY


async def waste_time(person: Person, spend_time: int) -> "Person":
    """
    Тратим время, в зависимости от скорости персонажа
    попутно увеличиваем голод и усталость,
    и проверяем живой ли персонаж
    """

    if spend_time < 1:
        return person

    # расчитываем время из скорости
    TOTAL = {
        person.speed > 9: 1,
        person.speed < 1: spend_time * 6,
        0 < person.speed < 10: spend_time * (6 - person.speed // 2),
    }[True]

    person.gametime += TOTAL

    if person.hunger + TOTAL > MAX_HUNGER:
        person.hunger = MAX_HUNGER
    else:
        person.hunger += TOTAL

    if person.weary + TOTAL > MAX_WEARY:
        person.weary = MAX_WEARY
    else:
        person.weary += TOTAL

    # если голод достиг максимума, вычитаем 1 здоровье
    if person.hunger == MAX_HUNGER:
        person.health -= 1
        if person.health < 1 and person.death is False:
            # значит персонаж умер сейчас от голода
            person.death = True
            person.death_reason = "смерть от голода"
            person.death_date = datetime.now()
    # аналогично с усталостью
    if person.weary == MAX_WEARY:
        person.mind -= 1
        if person.mind < 1 and person.death is False:
            # значит сошел с ума от усталости
            person.death = True
            person.death_reason = "смерть от нервного истощения"
            person.death_date = datetime.now()

    await person.update(**{_: getattr(person, _) for _ in person.to_dict()}).apply()

    return await Person.get(person.id)
