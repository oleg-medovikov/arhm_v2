from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime

from mdls import User, LocDescription


async def read_LocDescription(user: User) -> str:
    df = read_excel(
        "/tmp/_LocDescription.xlsx",
        usecols=[
            "id",
            "loc_id",
            "profession",
            "stage",
            "description",
            "stick_id",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in ["description"]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            else:
                row[key] = None

        for key in ["stick_id"]:
            if not isinstance(row[key], int):
                row[key] = None

        # если есть идентичная строчка пропускаем
        dialog = await LocDescription.query.where(
            and_(
                LocDescription.id == row["id"],
                LocDescription.loc_id == row["loc_id"],
                LocDescription.profession == row["profession"],
                LocDescription.stage == row["stage"],
                LocDescription.description == row["description"],
                LocDescription.stick_id == row["stick_id"],
            )
        ).gino.first()

        if dialog is not None:
            continue
        # есть есть строчка с такимже id - апдейтим
        action = await LocDescription.query.where(
            LocDescription.id == row["id"]
        ).gino.first()
        if action is not None:
            await action.update(
                loc_id=row["loc_id"],
                profession=row["profession"],
                stage=row["stage"],
                description=row["description"],
                stick_id=row["stick_id"],
                u_id=user.id,
                date_update=datetime.now(),
            ).apply()
            mess += f"\n Обновил строку {row['name']}"
            continue
        # или создаем новую строку
        await LocDescription.create(
            loc_id=row["loc_id"],
            profession=row["profession"],
            stage=row["stage"],
            description=row["description"],
            stick_id=row["stick_id"],
            u_id=user.id,
        )
        mess += f"\n Добавил строку {row['id']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
