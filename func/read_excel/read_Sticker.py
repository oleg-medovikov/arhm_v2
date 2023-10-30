from pandas import read_excel
from sqlalchemy import and_

from mdls import User, Sticker


async def read_Sticker(user: User) -> str:
    df = read_excel("/tmp/_Sticker.xlsx", usecols=["id", "name", "sticker_id"])

    mess = ""
    for row in df.to_dict("records"):
        # если есть идентичная строчка пропускаем
        sticker = await Sticker.query.where(
            and_(Sticker.name == row["name"], Sticker.sticker_id == row["sticker_id"])
        ).gino.first()

        if sticker is not None:
            continue
        # если нет, то создаем новую строку
        await Sticker.create(
            name=row["name"], sticker_id=row["sticker_id"], u_id=user.id
        )
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
