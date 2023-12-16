from pandas import DataFrame

from base import db
from mdls import User, Action


async def get_all_Action() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Action.id,
                Action.loc_id,
                Action.name,
                Action.dialog,
                Action.events,
                Action.weights,
                Action.demand,
                Action.person,
                Action.stage,
                User.fio,
                Action.date_update,
            ]
        )
        .select_from(Action.outerjoin(User))
        .order_by(Action.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "loc_id",
            "name",
            "dialog",
            "events",
            "weights",
            "demand",
            "person",
            "stage",
            "fio",
            "date_update",
        ],
    )

    return df
