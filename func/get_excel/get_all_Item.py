from pandas import DataFrame

from base import db
from mdls import User, Item


async def get_all_Item() -> "DataFrame":
    DATA = (
        await db.select(
            [
                Item.id,
                Item.name,
                Item.image_id,
                Item.description,
                Item.mess_equip,
                Item.mess_equip_fail,
                Item.mess_remove,
                Item.mess_remove_fail,
                Item.mess_drop,
                Item.type_kind,
                Item.slot,
                Item.emoji,
                Item.effect,
                Item.demand,
                Item.cost,
                Item.alternative,
                Item.single_use,
                Item.achievement,
                User.fio,
                Item.date_update,
            ]
        )
        .select_from(Item.outerjoin(User))
        .order_by(Item.id)
        .gino.all()
    )

    df = DataFrame(
        data=DATA,
        columns=[
            "id",
            "name",
            "image_id",
            "description",
            "mess_equip",
            "mess_equip_fail",
            "mess_remove",
            "mess_remove_fail",
            "mess_drop",
            "type_kind",
            "slot",
            "emoji",
            "effect",
            "demand",
            "cost",
            "alternative",
            "single_use",
            "achievement",
            "fio",
            "date_update",
        ],
    )

    return df
