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


def check(person: Person, DICT: dict) -> list:
    """
    проходим проверки на параметры персонажа,
    кидаем кубики нужное количество раз,
    добавляем влияние удачи
    возвращаем словарь с ходом прохождения проверки
    """
    list_ = []
    # проверок может быть в теории несколько
    for PARAM, VALUE in DICT.items():
        # если затесалась ошибка в параметре - игнорируем
        if PARAM not in DICT_CHECK.keys():
            print(f"ivent ошибка в check! {PARAM}, {VALUE}")
            continue
        if not isinstance(VALUE, int):
            if isinstance(VALUE, str) and not VALUE.isdigit():
                print(f"ivent ошибка в check! {PARAM}, {VALUE}")
                continue
            else:
                VALUE = int(VALUE)

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

        MESS = f"\n\nВы проходите проверку {DICT_CHECK.get(PARAM)}\n\n"
        MESS += f"всего у Вас {COUNT} бросков" + (
            f"\nи ещё {LUCK} благодаря удаче\n\n" if LUCK else "\n\n"
        )
        for _ in NUMBERS:
            MESS += f"  {_}\ufe0f\u20e3  "

        if bool(CHECK_PASSED):
            MESS += f"\n\nВам удалось пройти проверку {DICT_CHECK.get(PARAM)}!"
        else:
            MESS += f"\n\nВам не удалось пройти проверку {DICT_CHECK.get(PARAM)}"

        list_.append(
            {
                "param": PARAM,
                "sucsess": bool(CHECK_PASSED),
                "mess": MESS,
                "luck": LUCK,
                "count": COUNT,
                "numbers": NUMBERS,
                "CHECK_PASSED": CHECK_PASSED,
            }
        )

    return list_
