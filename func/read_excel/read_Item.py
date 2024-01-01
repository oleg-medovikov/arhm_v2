from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime
from json import loads

from mdls import User, Item


async def read_Item(user: User) -> str:
    df = read_excel(
        "/tmp/_Item.xlsx",
        usecols=[
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
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in ["demand", "effect"]:
            if isinstance(row[key], str):
                row[key] = loads(row[key].replace("'", '"').lower())
            else:
                row[key] = {}

        for key in ["image_id", "emoji"]:
            if not isinstance(row[key], int) or not isinstance(row[key], str):
                row[key] = None

        # делаем из False false
        row["single_use"] = bool(row["single_use"])
        row["achievement"] = bool(row["achievement"])

        for key in [
            "description",
            "mess_equip",
            "mess_equip_fail",
            "mess_remove",
            "mess_remove_fail",
            "mess_drop",
        ]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            else:
                row[key] = None

        # если есть идентичная строчка пропускаем
        item = await Item.query.where(
            and_(
                Item.id == row["id"],
                Item.name == row["name"],
                Item.stick_id == row["stick_id"],
                Item.description == row["description"],
                Item.mess_equip == row["mess_equip"],
                Item.mess_equip_fail == row["mess_equip_fail"],
                Item.mess_remove == row["mess_remove"],
                Item.mess_remove_fail == row["mess_remove_fail"],
                Item.mess_drop == row["mess_drop"],
                Item.type_kind == row["type_kind"],
                Item.slot == row["slot"],
                Item.emoji == row["emoji"],
                # Item.effect == row["effect"],
                # Item.demand == row["demand"],
                Item.cost == row["cost"],
                Item.alternative == row["alternative"],
                Item.single_use == row["single_use"],
                Item.achievement == row["achievement"],
            )
        ).gino.first()

        if item is not None:
            continue
        # если есть строчка с таким же name то делаем update
        item = await Item.query.where(Item.name == row["name"]).gino.first()
        if item is not None:
            await item.update(
                name=row["name"],
                image_id=row["image_id"],
                description=row["description"],
                mess_equip=row["mess_equip"],
                mess_equip_fail=row["mess_equip_fail"],
                mess_remove=row["mess_remove"],
                mess_remove_fail=row["mess_remove_fail"],
                mess_drop=row["mess_drop"],
                type_kind=row["type_kind"],
                slot=row["slot"],
                emoji=row["emoji"],
                effect=row["effect"],
                demand=row["demand"],
                cost=row["cost"],
                alternative=row["alternative"],
                single_use=row["single_use"],
                achievement=row["achievement"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\n Обновил строку {row['name']}"
            continue
        # если нет, то создаем новую строку
        await Item.create(
            name=row["name"],
            image_id=row["image_id"],
            description=row["description"],
            mess_equip=row["mess_equip"],
            mess_equip_fail=row["mess_equip_fail"],
            mess_remove=row["mess_remove"],
            mess_remove_fail=row["mess_remove_fail"],
            mess_drop=row["mess_drop"],
            type_kind=row["type_kind"],
            slot=row["slot"],
            emoji=row["emoji"],
            effect=row["effect"],
            demand=row["demand"],
            cost=row["cost"],
            alternative=row["alternative"],
            single_use=row["single_use"],
            achievement=row["achievement"],
            u_id=user.id,
        )
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
