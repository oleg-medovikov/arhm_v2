from disp.excel import router
from aiogram.types import Message
from aiogram import F, Bot

from func import (
    delete_message,
    read_MessText,
    read_Location,
    read_PersonDefault,
    read_Sticker,
    read_Item,
    read_Dialog,
    read_Action,
    read_Event,
)
from mdls import User


@router.message(F.content_type.in_(["document"]))
async def update_base(message: Message, bot: Bot):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    if message.document is None:
        return
    if " " in str(message.document.file_name):
        file_name = str(message.document.file_name).split(" ")[0] + ".xlsx"
    else:
        file_name = str(message.document.file_name)

    FUNC = {
        "MessText.xlsx": read_MessText(user),
        "Location.xlsx": read_Location(user),
        "PersonDefault.xlsx": read_PersonDefault(user),
        "Sticker.xlsx": read_Sticker(user),
        "Item.xlsx": read_Item(user),
        "Dialog.xlsx": read_Dialog(user),
        "Action.xlsx": read_Action(user),
        "Event.xlsx": read_Event(user),
    }.get(file_name)

    if FUNC is None:
        return

    file = await bot.get_file(message.document.file_id)
    await bot.download_file(str(file.file_path), f"/tmp/_{file_name}")

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
