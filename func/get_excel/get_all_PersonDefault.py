from pandas import DataFrame

from base import db
from mdls import User, PersonDefault


async def get_all_PersonDefault() -> "DataFrame":
    DATA = (
        await db.select(
            [
                PersonDefault.profession,
                PersonDefault.start_loc_id,
                PersonDefault.start_items,
                PersonDefault.money_min,
                PersonDefault.money_max,
                PersonDefault.healf_min,
                PersonDefault.healf_max,
                PersonDefault.mind_min,
                PersonDefault.mind_max,
                PersonDefault.speed_min,
                PersonDefault.speed_max,
                PersonDefault.stealth_min,
                PersonDefault.stealth_max,
                PersonDefault.strength_min,
                PersonDefault.strength_max,
                PersonDefault.knowledge_min,
                PersonDefault.knowledge_max,
                PersonDefault.godliness_min,
                PersonDefault.godliness_max,
                PersonDefault.luck_min,
                PersonDefault.luck_max,
                User.fio,
                PersonDefault.date_update,
            ]
        )
        .select_from(PersonDefault.outerjoin(User))
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "profession",
            "start_loc_id",
            "start_items",
            "money_min",
            "money_max",
            "healf_min",
            "healf_max",
            "mind_min",
            "mind_max",
            "speed_min",
            "speed_max",
            "stealth_min",
            "stealth_max",
            "strength_min",
            "strength_max",
            "knowledge_min",
            "knowledge_max",
            "godliness_min",
            "godliness_max",
            "luck_min",
            "luck_max",
            "fio",
            "date_update",
        ],
    )

    return df
