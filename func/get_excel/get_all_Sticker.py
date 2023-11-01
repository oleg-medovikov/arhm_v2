from pandas import DataFrame

from base import db
from mdls import User, Sticker


async def get_all_Sticker() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Sticker.id,
                Sticker.name,
                Sticker.category,
                Sticker.unique_id,
                Sticker.send_id,
                User.fio,
                Sticker.date_update,
            ]
        )
        .select_from(Sticker.outerjoin(User))
        .order_by(Sticker.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "name",
            "category",
            "unique_id",
            "send_id",
            "fio",
            "date_update",
        ],
    )

    return df
