from pandas import read_excel
from sqlalchemy import and_
from ast import literal_eval
from datetime import datetime

from mdls import User, Action


async def read_Action(user: User) -> str:
    df = read_excel(
        "/tmp/_Action.xlsx",
        usecols=[
            "id",
            "loc_id",
            "name",
            "dialog",
            "events",
            "weights",
            "demand",
            "profession",
            "stage",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in ["demand", "events", "weights"]:
            if isinstance(row[key], str):
                row[key] = literal_eval(row[key].lower())
            else:
                row[key] = None

        for key in ["dialog"]:
            if not isinstance(row[key], int):
                row[key] = None

        # если есть идентичная строчка пропускаем
        dialog = await Action.query.where(
            and_(
                Action.id == row["id"],
                Action.loc_id == row["loc_id"],
                Action.name == row["name"],
                Action.dialog == row["dialog"],
                Action.events == row["events"],
                Action.weights == row["weights"],
                Action.profession == row["profession"],
                Action.stage == row["stage"],
            )
        ).gino.first()

        if dialog is not None:
            continue
        # есть есть строчка с такимже id - апдейтим
        action = await Action.query.where(Action.id == row["id"]).gino.first()
        if action is not None:
            await action.update(
                loc_id=row["loc_id"],
                name=row["name"],
                dialog=row["dialog"],
                events=row["events"],
                weights=row["weights"],
                demand=row["demand"],
                profession=row["profession"],
                stage=row["stage"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\nОбновил строку: {row['name']}"
            continue
        # или создаем новую строку
        await Action.create(
            loc_id=row["loc_id"],
            name=row["name"],
            dialog=row["dialog"],
            events=row["events"],
            weights=row["weights"],
            demand=row["demand"],
            profession=row["profession"],
            stage=row["stage"],
            u_id=user.id,
        )
        mess += f"\nДобавил строку: {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
