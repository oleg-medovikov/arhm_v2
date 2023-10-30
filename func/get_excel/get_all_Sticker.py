from pandas import DataFrame

from base import db
from mdls import User, Sticker


async def get_all_Sticker() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Sticker.id,
                Sticker.name,
                Sticker.sticker_id,
                User.fio,
                Sticker.date_update,
            ]
        )
        .select_from(Sticker.outerjoin(User))
        .gino.all()
    )

    df = DataFrame(
        data=DATA, columns=["id", "name", "sticker_id", "fio", "date_update"]
    )

    return df
