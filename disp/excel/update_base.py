from aiogram.types import Message
from aiogram import F

from disp import dp, bot
from func import (
    delete_message,
    read_MessText,
    read_Location,
    read_PersonDefault,
    read_Sticker,
    read_Item,
)
from mdls import User


@dp.message(F.content_type.in_(["document"]))
async def update_base(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    if message.document is None:
        return

    FUNC = {
        "MessText.xlsx": read_MessText(user),
        "Location.xlsx": read_Location(user),
        "PersonDefaults.xlsx": read_PersonDefault(user),
        "Sticker.xlsx": read_Sticker(user),
        "Item.xlsx": read_Item(user),
    }.get(str(message.document.file_name))

    if FUNC is None:
        return

    file = await bot.get_file(message.document.file_id)
    await bot.download_file(str(file.file_path), f"/tmp/_{message.document.file_name}")

    try:
        mess = await FUNC
    except Exception as e:
        return await message.answer(
            str(e), disable_notification=True, parse_mode="Markdown"
        )
    else:
        return await message.answer(
            mess.replace("_", "\\_"), disable_notification=True, parse_mode="Markdown"
        )
