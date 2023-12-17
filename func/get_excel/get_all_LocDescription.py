from pandas import DataFrame

from base import db
from mdls import User, LocDescription, Location


async def get_all_LocDescription() -> "DataFrame":
    DATA = (
        await db.select(
            [
                LocDescription.id,
                LocDescription.loc_id,
                Location.name,
                Location.district,
                LocDescription.profession,
                LocDescription.stage,
                LocDescription.description,
                LocDescription.stick_id,
                User.fio,
                LocDescription.date_update,
            ]
        )
        .select_from(LocDescription.join(User).join(Location))
        .order_by(LocDescription.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "loc_id",
            "location",
            "district",
            "profession",
            "stage",
            "description",
            "stick_id",
            "fio",
            "date_update",
        ],
    )

    return df
