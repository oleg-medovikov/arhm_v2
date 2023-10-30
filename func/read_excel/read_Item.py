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
            "stick_id",
            "description",
            "mess_equip",
            "mess_fail",
            "mess_remove",
            "mess_drop",
            "type_kind",
            "slot",
            "emoji",
            "effect",
            "demand",
            "cost",
            "single_use",
            "achievement",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        # делаем из False false
        if row['demand'] is not None:
            row['demand'] = loads(row['demand'].replace("'", '"').lower())
        if row['effect'] is not None:
            row['effect'] = loads(row['effect'].replace("'", '"').lower())

        row['single_use'] = bool(row['single_use'])
        row['achievement'] = bool(row['achievement'])

        # если есть идентичная строчка пропускаем
        item = await Item.query.where(
            and_(
                Item.id == row["id"],
                Item.name == row["name"],
                Item.stick_id == row["stick_id"],
                Item.description == row["description"],
                Item.mess_equip == row["mess_equip"],
                Item.mess_fail == row["mess_fail"],
                Item.mess_remove == row["mess_remove"],
                Item.mess_drop == row["mess_drop"],
                Item.type_kind == row["type_kind"],
                Item.slot == row["slot"],
                Item.emoji == row["emoji"],
                # Item.effect == row["effect"],
                # Item.demand == row["demand"],
                Item.cost == row["cost"],
                Item.single_use == row["single_use"],
                Item.achievement == row["achievement"],
            )
        ).gino.first()

        if item is not None:
            continue
        # если есть строчка с таким же name то делаем update
        item = await Item.query.where(Item.name == row["name"]).gino.first()
        print(item)
        if item is not None:
            await item.update(
                name=row["name"],
                stick_id=row["stick_id"],
                description=row["description"],
                mess_equip=row["mess_equip"],
                mess_fail=row["mess_fail"],
                mess_remove=row["mess_remove"],
                mess_drop=row["mess_drop"],
                type_kind=row["type_kind"],
                slot=row["slot"],
                emoji=row["emoji"],
                effect=row["effect"],
                demand=row["demand"],
                cost=row["cost"],
                single_use=row["single_use"],
                achievement=row["achievement"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\n Обновил строку {row['name']}"
            continue
        # если нет, то создаем новую строку
        print('test')
        await Item.create(
            name=row["name"],
            stick_id=row["stick_id"],
            description=row["description"],
            mess_equip=row["mess_equip"],
            mess_fail=row["mess_fail"],
            mess_remove=row["mess_remove"],
            mess_drop=row["mess_drop"],
            type_kind=row["type_kind"],
            slot=row["slot"],
            emoji=row["emoji"],
            effect=row["effect"],
            demand=row["demand"],
            cost=row["cost"],
            single_use=row["single_use"],
            achievement=row["achievement"],               
            u_id=user.id,
                )
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
