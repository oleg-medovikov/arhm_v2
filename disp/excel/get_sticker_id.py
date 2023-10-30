from aiogram.types import Message
from aiogram import F

from disp import dp, bot
from func import delete_message
from mdls import User


@dp.message(F.content_type.in_(["sticker"]))
async def get_sticker_id(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    if message.sticker is None:
        return

    mess = f"я принял стикер! его id \n {message.sticker.file_id}".replace("_", "\\_")

    await message.answer(mess, disable_notification=True, parse_mode="Markdown")
    await bot.send_sticker(message.chat.id, sticker=message.sticker.file_id)
