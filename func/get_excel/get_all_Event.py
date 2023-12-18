from pandas import DataFrame

from base import db
from mdls import User, Event


async def get_all_Event() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Event.id,
                Event.name,
                Event.description,
                Event.stick_id,
                Event.single_use,
                Event.waste_time,
                Event.monster,
                Event.demand,
                Event.mess_prise,
                Event.mess_punish,
                Event.prise,
                Event.punish,
                User.fio,
                Event.date_update,
            ]
        )
        .select_from(Event.join(User))
        .order_by(Event.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "name",
            "description",
            "stick_id",
            "single_use",
            "waste_time",
            "monster",
            "demand",
            "mess_prise",
            "mess_punish",
            "prise",
            "punish",
            "fio",
            "date_update",
        ],
    )

    return df
