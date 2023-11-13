from datetime import datetime, timedelta

from mdls import Person
from conf import emoji
from .str_weary import str_weary
from .str_hunger import str_hunger


def person_status_card(PERS: "Person") -> str:
    "генерируем краткую карточку состояния персонажа"

    DATE = datetime.fromisoformat(str(PERS.create_date)).strftime("%d.%m.%Y в %H:%M")
    DAYS = PERS.gametime // 96
    TIME = (
        datetime.strptime("09:00", "%H:%M") + timedelta(minutes=15 * PERS.gametime)
    ).strftime("%H:%M")

    LIST = (
        "*Карточка персонажа*\n",
        "*ИМЯ:* ",
        PERS.gamename,
        ", ",
        PERS.profession,
        "\n*Зарегистрирован",
        ("" if PERS.sex else "а"),
        ":* ",
        DATE,
        "\n*Проведено дней в Археме:* ",
        DAYS,
        "\n ``` \n",
        emoji("clock"),
        "  ",
        TIME,
        "  ",
        emoji("dollar"),
        " ",
        PERS.money,
        "  ",
        emoji("proof"),
        "  ",
        PERS.proof,
        "\n",
        emoji("heart"),
        " ",
        PERS.health,
        " из ",
        PERS.health_max,
        "\n",
        emoji("brain"),
        " ",
        PERS.mind,
        " из ",
        PERS.mind_max,
        "\n\n",
        emoji("strength"),
        " ",
        PERS.strength,
        " " * (4 - len(str(PERS.strength))),
        emoji("speed"),
        " ",
        PERS.speed,
        " " * (4 - len(str(PERS.speed))),
        emoji("stealth"),
        " ",
        PERS.stealth,
        "\n",
        emoji("knowledge"),
        " ",
        PERS.knowledge,
        " " * (4 - len(str(PERS.knowledge))),
        emoji("godliness"),
        " ",
        PERS.godliness,
        " " * (4 - len(str(PERS.godliness))),
        emoji("luck"),
        " ",
        PERS.luck,
        "\n\n",
        emoji("hunger"),
        " ",
        str_hunger(PERS.hunger),
        "\n",
        emoji("weary"),
        " ",
        str_weary(PERS.weary),
        "\n ``` \n",
        "*Достижения:*\n",
        "нет",
    )

    MESS = "".join(str(x) for x in LIST)

    return MESS
