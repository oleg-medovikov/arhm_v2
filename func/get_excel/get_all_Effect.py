from pandas import DataFrame

from base import db
from mdls import User, Effect


async def get_all_Effect() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Effect.id,
                Effect.name,
                Effect.impact,
                Effect.duration,
                Effect.emoji,
                Effect.stages,
                User.fio,
                Effect.date_update,
            ]
        )
        .select_from(Effect.outerjoin(User))
        .order_by(Effect.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "name",
            "impact",
            "duration",
            "emoji",
            "stages",
            "fio",
            "date_update",
        ],
    )

    return df
