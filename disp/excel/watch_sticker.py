from aiogram.types import Message
from aiogram import F

from disp import dp, bot
from func import delete_message
from mdls import User, Sticker


@dp.message(F.text.startswith("sticker"))
async def watch_sticker(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    try:
        number = int(str(message.text).split(" ")[-1])
    except Exception:
        mess = "не нашел номера в сообщении"
        return await message.answer(
            mess, disable_notification=True, parse_mode="Markdown"
        )

    sticker = await Sticker.get(number)

    if sticker is None:
        mess = f"нет стикера с id {number}"
        return await message.answer(
            mess, disable_notification=True, parse_mode="Markdown"
        )

    await bot.send_sticker(message.chat.id, sticker=sticker.sticker_id)
    mess = f"id: {sticker.id}  " + sticker.name
    await message.answer(mess, disable_notification=True, parse_mode="Markdown")
