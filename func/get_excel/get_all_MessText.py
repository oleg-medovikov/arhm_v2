from pandas import DataFrame

from base import db
from mdls import User, MessText


async def get_all_MessText() -> "DataFrame":
    DATA = (
        await db.select([MessText.name, MessText.text, User.fio, MessText.date_update])
        .select_from(MessText.outerjoin(User))
        .gino.all()
    )

    df = DataFrame(data=DATA, columns=["name", "text", "fio", "date_update"])

    return df
