from pandas import DataFrame

from base import db
from mdls import User, Dialog


async def get_all_Dialog() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Dialog.d_id,
                Dialog.q_id,
                Dialog.stick_id,
                Dialog.name,
                Dialog.question,
                Dialog.answers,
                Dialog.transfer,
                Dialog.demand,
                Dialog.spend_time,
                Dialog.buy_items,
                Dialog.buy_costs,
                Dialog.sale_items,
                User.fio,
                Dialog.date_update,
            ]
        )
        .select_from(Dialog.outerjoin(User))
        .order_by(Dialog.d_id, Dialog.q_id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "d_id",
            "q_id",
            "stick_id",
            "name",
            "question",
            "answers",
            "transfer",
            "demand",
            "spend_time",
            "buy_items",
            "buy_costs",
            "sale_items",
            "sale_costs",
            "fio",
            "date_update",
        ],
    )

    return df
