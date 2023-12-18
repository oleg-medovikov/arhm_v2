from pandas import DataFrame

from base import db
from mdls import User, Action, Location


async def get_all_Action() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Action.id,
                Action.loc_id,
                Location.name,
                Location.district,
                Action.name,
                Action.dialog,
                Action.events,
                Action.weights,
                Action.demand,
                Action.profession,
                Action.stage,
                User.fio,
                Action.date_update,
            ]
        )
        .select_from(Action.join(User).join(Location))
        .order_by(Action.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "loc_id",
            "location",
            "district",
            "name",
            "dialog",
            "events",
            "weights",
            "demand",
            "profession",
            "stage",
            "fio",
            "date_update",
        ],
    )

    return df
