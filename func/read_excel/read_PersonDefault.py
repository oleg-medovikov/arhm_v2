from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime
from json import loads

from mdls import User, PersonDefault


async def read_PersonDefault(user: User) -> str:
    df = read_excel(
        "/tmp/_PersonDefault.xlsx",
        usecols=[
            "profession",
            "start_loc_id",
            "start_items",
            "money_min",
            "money_max",
            "health_min",
            "health_max",
            "mind_min",
            "mind_max",
            "speed_min",
            "speed_max",
            "stealth_min",
            "stealth_max",
            'strength_min',
            'strength_max',
            "knowledge_min",
            "knowledge_max",
            "godliness_min",
            "godliness_max",
            "luck_min",
            "luck_max",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        # если есть идентичная строчка пропускаем
        defaults = await PersonDefault.query.where(
            and_(
                PersonDefault.profession==row['profession'],
                PersonDefault.start_loc_id==row['start_loc_id'],
                PersonDefault.start_items==loads(row['start_items']),
                PersonDefault.money_min==row['money_min'],
                PersonDefault.money_max==row['money_max'],
                PersonDefault.health_min==row['health_min'],
                PersonDefault.health_max==row['health_max'],
                PersonDefault.mind_min==row['mind_min'],
                PersonDefault.mind_max==row['mind_max'],
                PersonDefault.speed_min==row['speed_min'],
                PersonDefault.speed_max==row['speed_max'],
                PersonDefault.stealth_min==row['stealth_min'],
                PersonDefault.stealth_max==row['stealth_max'],
                PersonDefault.strength_min==row['strength_min'],
                PersonDefault.strength_max==row['strength_max'],
                PersonDefault.knowledge_min==row['knowledge_min'],
                PersonDefault.knowledge_max==row['knowledge_max'],
                PersonDefault.godliness_min==row['godliness_min'],
                PersonDefault.godliness_max==row['godliness_max'],
                PersonDefault.luck_min==row['luck_min'],
                PersonDefault.luck_max==row['luck_max'],
                )
        ).gino.first()

        if defaults is not None:
            continue
        # если есть строчка с таким же name то делаем update
        defaults = await PersonDefault.query.where(
            PersonDefault.profession == row["profession"]
        ).gino.first()
        if defaults is not None:
            await defaults.update(
                profession=row['profession'],
                start_loc_id=row['start_loc_id'],
                start_items=loads(row['start_items']),
                money_min=row['money_min'],
                money_max=row['money_max'],
                health_min=row['health_min'],
                health_max=row['health_max'],
                mind_min=row['mind_min'],
                mind_max=row['mind_max'],
                speed_min=row['speed_min'],
                speed_max=row['speed_max'],
                stealth_min=row['stealth_min'],
                stealth_max=row['stealth_max'],
                strength_min=row['strength_min'],
                strength_max=row['strength_max'],
                knowledge_min=row['knowledge_min'],
                knowledge_max=row['knowledge_max'],
                godliness_min=row['godliness_min'],
                godliness_max=row['godliness_max'],
                luck_min=row['luck_min'],
                luck_max=row['luck_max'],
                u_id=user.id,
                date_update=datetime.now()
            ).apply()
            mess += f"\n Обновил строку {row['profession']}"
            continue
        # если нет, то создаем новую строку
        await PersonDefault.create(
            profession=row['profession'],
            start_loc_id=row['start_loc_id'],
            start_items=loads(row['start_items']),
            money_min=row['money_min'],
            money_max=row['money_max'],
            health_min=row['health_min'],
            health_max=row['health_max'],
            mind_min=row['mind_min'],
            mind_max=row['mind_max'],
            speed_min=row['speed_min'],
            speed_max=row['speed_max'],
            stealth_min=row['stealth_min'],
            stealth_max=row['stealth_max'],
            strength_min=row['strength_min'],
            strength_max=row['strength_max'],
            knowledge_min=row['knowledge_min'],
            knowledge_max=row['knowledge_max'],
            godliness_min=row['godliness_min'],
            godliness_max=row['godliness_max'],
            luck_min=row['luck_min'],
            luck_max=row['luck_max'],
            u_id=user.id
        )
        mess += f"\n Добавил строку {row['profession']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
