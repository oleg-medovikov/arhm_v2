from pandas import read_excel
from sqlalchemy import and_
from ast import literal_eval
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

from mdls import User, Effect


async def read_Effect(user: User) -> str:
    df = read_excel(
        "/tmp/_Effect.xlsx",
        usecols=[
            "id",
            "name",
            "impact",
            "duration",
            "emoji",
            "stages",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in ["impact", "stages"]:
            if isinstance(row[key], str):
                row[key] = literal_eval(row[key].lower())
            else:
                row[key] = None

        for key in ["emoji"]:
            if not isinstance(row[key], str):
                row[key] = None

        # если есть идентичная строчка пропускаем
        dialog = await Effect.query.where(
            and_(
                Effect.id == row["id"],
                Effect.name == row["name"],
                Effect.impact == row["impact"],
                Effect.duration == row["duration"],
                Effect.emoji == row["emoji"],
                Effect.stages == row["stages"],
            )
        ).gino.first()

        if dialog is not None:
            continue
        # есть есть строчка с такимже id - апдейтим
        action = await Effect.query.where(Effect.id == row["id"]).gino.first()
        if action is not None:
            await action.update(
                name=row["name"],
                impact=row["impact"],
                duration=row["duration"],
                emoji=row["emoji"],
                stages=row["stages"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\nОбновил строку: {row['name']}"
            continue
        # или создаем новую строку
        await Effect.create(
            name=row["name"],
            impact=row["impact"],
            duration=row["duration"],
            emoji=row["emoji"],
            stages=row["stages"],
            u_id=user.id,
        )
        mess += f"\nДобавил строку: {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
