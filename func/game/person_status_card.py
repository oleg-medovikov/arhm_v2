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
        f"*Карточка персонажа*\n*Имя:* {PERS.gamename}, {PERS.profession}",
        f'\n*Зарегистрирован{("" if PERS.sex else "а")}:* {DATE}',
        f"\n*Проведено дней в Археме:* {DAYS}",
        # "\n ``` ",
        f'\n\n{emoji("clock")}  {TIME}  {emoji("dollar")}  {PERS.money}  {emoji("proof")}  {PERS.proof}',
        f'\n\n{emoji("heart")}  {PERS.health} из {PERS.health_max}  {emoji("brain")}  {PERS.mind} из {PERS.mind_max}',
        f'\n\n{emoji("strength")}  {PERS.strength}{" " * (4 - len(str(PERS.strength)))}',
        f'{emoji("speed")}  {PERS.speed}{" " * (4 - len(str(PERS.speed)))}',
        f'{emoji("stealth")}  {PERS.stealth}',
        f'\n{emoji("knowledge")}  {PERS.knowledge}{" " * (4 - len(str(PERS.knowledge)))}',
        f'{emoji("godliness")}  {PERS.godliness}{" " * (4 - len(str(PERS.godliness)))}',
        f'{emoji("luck")}  {PERS.luck}',
        f'\n\n{emoji("swords")} {PERS.dmg_fight}   {emoji("magic")} {PERS.dmg_magic}'
        f'\n\n{emoji("hunger")} {str_hunger(PERS.hunger)}',
        f'\n{emoji("weary")} {str_weary(PERS.weary)}',
        # "\n ``` ",
        "\n\n*Эффекты:*",
        "\nнет",
    )

    MESS = "".join(str(x) for x in LIST)

    return MESS
