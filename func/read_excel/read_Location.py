from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime
from json import loads

from mdls import User, Location


async def read_Location(user: User) -> str:
    df = read_excel(
        "/tmp/_Location.xlsx",
        usecols=["id", "name", "declension", "contact_list", "district", "district_id"],
    )

    mess = ""
    for row in df.to_dict("records"):
        # если есть идентичная строчка пропускаем
        location = await Location.query.where(
            and_(
                Location.id == row["id"],
                Location.name == row["name"],
                Location.declension == row["declension"],
                Location.contact_list == loads(row["contact_list"]),
                Location.district == row["district"],
                Location.district_id == row["district_id"],
            )
        ).gino.first()

        if location is not None:
            continue
        # если есть строчка с таким же name то делаем update
        location = await Location.query.where(Location.id == row["id"]).gino.first()
        if location is not None:
            await location.update(
                name=row["name"],
                declension=row["declension"],
                contact_list=loads(row["contact_list"]),
                district=row["district"],
                district_id=row["district_id"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\n Обновил строку {row['name']}"
            continue
        # если нет, то создаем новую строку
        await Location.create(
            id=row["id"],
            name=row["name"],
            declension=row["declension"],
            contact_list=loads(row["contact_list"]),
            district=row["district"],
            district_id=row["district_id"],
            u_id=user.id,
        )
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
