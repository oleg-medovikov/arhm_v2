from pandas import read_excel
from sqlalchemy import and_
from ast import literal_eval

from mdls import User, Dialog


async def read_Dialog(user: User) -> str:
    df = read_excel(
        "/tmp/_Dialog.xlsx",
        usecols=[
            "d_id",
            "q_id",
            "image_id",
            "name",
            "question",
            "answers",
            "transfer",
            "demand",
            "spend_time",
            "buy_items",
            "buy_costs",
            "sale_items",
            "sale_costs",
        ],
    )

    mess = ""
    for row in df.to_dict("records"):
        for key in [
            "demand",
            "answers",
            "transfer",
            "buy_items",
            "buy_costs",
            "spend_time",
            "sale_items",
            "sale_costs",
        ]:
            if isinstance(row[key], str):
                row[key] = literal_eval(row[key].lower())
            else:
                row[key] = None

        for key in ["question"]:
            if isinstance(row[key], str):
                row[key] = row[key].replace("\u2028", "\n")
            else:
                row[key] = None

        # если есть идентичная строчка пропускаем
        dialog = await Dialog.query.where(
            and_(
                Dialog.d_id == row["d_id"],
                Dialog.q_id == row["q_id"],
                Dialog.image_id == row["image_id"],
                Dialog.name == row["name"],
                Dialog.question == row["question"],
            )
        ).gino.first()

        if dialog is not None:
            await dialog.delete()

        # и создаем новую строку
        await Dialog.create(
            d_id=row["d_id"],
            q_id=row["q_id"],
            image_id=row["image_id"],
            name=row["name"],
            question=row["question"],
            answers=row["answers"],
            transfer=row["transfer"],
            demand=row["demand"],
            spend_time=row["spend_time"],
            buy_items=row["buy_items"],
            buy_costs=row["buy_costs"],
            sale_items=row["sale_items"],
            sale_costs=row["sale_items"],
            u_id=user.id,
        )
        mess += f"\nДобавил строку: {row['d_id']} {row['q_id']}"

    if mess == "":
        mess = "Нечего изменять"

    return mess
