from pandas import read_excel
from sqlalchemy import and_
from datetime import datetime

from mdls import User, MessText


async def read_MessText(user: User) -> str:
    df = read_excel("/tmp/_MessText.xlsx", usecols=["name", "text"])

    mess = ""
    for row in df.to_dict("records"):
        # если есть идентичная строчка пропускаем
        mess_text = await MessText.query.where(
            and_(MessText.name == row["name"], MessText.text == row["text"])
        ).gino.first()

        if mess_text is not None:
            continue
        # если есть строчка с таким же name то делаем update
        mess_text = await MessText.query.where(
            MessText.name == row["name"]
        ).gino.first()
        if mess_text is not None:
            await mess_text.update(
                text=row["text"], u_id=user.id, date_update=datetime.now()
            ).apply()
            mess += f"\n Обновил строку {row['name']}"
            continue
        # если нет, то создаем новую строку
        await MessText.create(name=row["name"], text=row["text"], u_id=user.id)
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
