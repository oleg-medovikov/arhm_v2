from mdls import Person
from random import randint


DICT_CHECK = {
    "speed": "на скорость",
    "stealth": "на незаметность",
    "strength": "на силу",
    "knowledge": "на осведомлённость в данном вопросе",
    "godliness": "на Вашу веру в высшие силы",
    "luck": "на удачу",
}


async def check(person: Person, DICT: dict) -> list:
    """
    проходим проверки на параметры персонажа,
    кидаем кубики нужное количество раз,
    добавляем влияние удачи
    возвращаем словарь с ходом прохождения проверки
    """
    list_ = []
    for PARAM, VALUE in DICT.items():
        # проверок может быть в теории несколько
        if PARAM not in DICT_CHECK.keys():
            # если затесалась ошибка в параметре - игнорируем
            print(f"ivent ошибка в check! {PARAM}")
            continue

        # 5% шанс дополнительного броска за каждую единицу удачи
        LUCK = sum(randint(0, 100) // 95 for _ in range(person.luck))
        COUNT = getattr(person, PARAM) - VALUE
        # кидаем кубики
        NUMBERS = [randint(1, 6) for _ in range(COUNT + LUCK)]
        # проверяем благословение
        CHECK_LIST = {
            person.bless == 0: [5, 6],
            person.bless > 0: [4, 5, 6],
            person.bless < 0: [6],
        }[True]
        # считаем количество успешных проверок
        CHECK_PASSED = sum([NUMBERS.count(x) for x in CHECK_LIST])

        # нужно сформировать сообщение

        MESS = f"\n\nВы проходите проверку {DICT_CHECK.get(PARAM)}\n"
        MESS += f"всего у Вас попыток: {COUNT}" + (
            f" из которых {LUCK} благодаря удаче\n" if LUCK else "\n"
        )
        for _ in NUMBERS:
            MESS += f"  {_}\ufe0f\u20e3  "

        if not bool(CHECK_PASSED):
            MESS += f"\nВам не удалось пройти проверку {DICT_CHECK.get(PARAM)}"
        else:
            MESS += f"\nВам удалось пройти проверку {DICT_CHECK.get(PARAM)}!"

        list_.append(
            {
                "param": PARAM,
                "mess": MESS,
                "luck": LUCK,
                "count": COUNT,
                "numbers": NUMBERS,
                "CHECK_PASSED": CHECK_PASSED,
            }
        )

    return list_
