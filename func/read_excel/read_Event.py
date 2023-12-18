from pandas import read_excel
from sqlalchemy import and_
from ast import literal_eval
from datetime import datetime

from mdls import User, Event


async def read_Event(user: User) -> str:
    df = read_excel(
        "/tmp/_Event.xlsx",
        usecols=[
            "id",
            "name",
            "description",
            "stick_id",
            "single_use",
            "spend_time",
            "monster",
            "demand",
            "mess_prise",
            "mess_punish",
            "prise",
            "punish",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in ["demand", "prise", "punish"]:
            if isinstance(row[key], str):
                row[key] = literal_eval(row[key].lower())
            else:
                row[key] = None

        for key in ["monster", "stick_id"]:
            if not isinstance(row[key], int):
                row[key] = None

        for key in ["single_use"]:
            if not isinstance(row[key], bool):
                row[key] = bool(row[key])

        for key in ["description", "mess_prise", "mess_punish"]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            else:
                row[key] = None

        # если есть идентичная строчка пропускаем
        dialog = await Event.query.where(
            and_(
                Event.id == row["id"],
                Event.name == row["name"],
                Event.description == row["description"],
                Event.stick_id == row["stick_id"],
                Event.single_use == row["single_use"],
                Event.spend_time == row["spend_time"],
                Event.monster == row["monster"],
                Event.mess_prise == row["mess_prise"],
                Event.mess_punish == row["mess_punish"],
            )
        ).gino.first()

        if dialog is not None:
            continue
        # есть есть строчка с такимже id - апдейтим
        action = await Event.query.where(Event.id == row["id"]).gino.first()
        if action is not None:
            await action.update(
                name=row["name"],
                description=row["description"],
                stick_id=row["stick_id"],
                single_use=row["single_use"],
                spend_time=row["spend_time"],
                monster=row["monster"],
                demand=row["demand"],
                prise=row["prise"],
                punish=row["punish"],
                mess_prise=row["mess_prise"],
                mess_punish=row["mess_punish"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\nОбновил строку: {row['name']}"
            continue
        # или создаем новую строку
        await Event.create(
            name=row["name"],
            description=row["description"],
            stick_id=row["stick_id"],
            single_use=row["single_use"],
            spend_time=row["spend_time"],
            monster=row["monster"],
            demand=row["demand"],
            prise=row["prise"],
            punish=row["punish"],
            mess_prise=row["mess_prise"],
            mess_punish=row["mess_punish"],
            u_id=user.id,
        )
        mess += f"\nДобавил строку: {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
