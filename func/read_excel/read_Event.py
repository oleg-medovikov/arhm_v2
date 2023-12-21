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
            "write_to_note",
            "waste_time",
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

        for key in ["single_use", "write_to_note"]:
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
                Event.write_to_note == row["write_to_note"],
                Event.waste_time == row["waste_time"],
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
            row["u_id"] = user.id
            row["date_update"] = datetime.now()
            await action.update(
                **{
                    key: value
                    for key, value in row.items()
                    if key in Event.__table__.columns
                }
            ).apply()
            mess += f"\nОбновил строку: {row['name']}"
            continue

        # или создаем новую строку
        row["u_id"] = user.id
        await Event.create(
            **{
                key: value
                for key, value in row.items()
                if key in Event.__table__.columns
            }
        )
        mess += f"\nДобавил строку: {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
