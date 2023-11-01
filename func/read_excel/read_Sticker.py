from pandas import read_excel

from mdls import User, Sticker


async def read_Sticker(user: User) -> str:
    df = read_excel(
        "/tmp/_Sticker.xlsx", usecols=["name", "category", "unique_id", "send_id"]
    )

    mess = ""
    for row in df.to_dict("records"):
        # удаляем лишние пробелы, это важно!
        row["send_id"] = row["send_id"].strip()
        row["unique_id"] = row["unique_id"].strip()

        # если есть идентичная строчка пропускаем
        sticker = await Sticker.query.where(
            Sticker.unique_id == row["unique_id"]
        ).gino.first()

        if sticker is not None:
            continue
        # если нет, то создаем новую строку
        await Sticker.create(
            name=row["name"],
            category=row["category"],
            unique_id=["unique_id"],
            send_id=row["sticker_id"],
            u_id=user.id,
        )
        mess += f"\n Добавил строку {row['name']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
