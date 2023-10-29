from pandas import DataFrame

from base import db
from mdls import User, Location


async def get_all_Location() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Location.id,
                Location.name,
                Location.declension,
                Location.contact_list,
                Location.district,
                Location.district_id,
                User.fio,
                Location.date_update,
            ]
        )
        .select_from(Location.outerjoin(User))
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "name",
            "declension",
            "contact_list",
            "district",
            "district_id",
            "fio",
            "date_update",
        ],
    )

    return df
