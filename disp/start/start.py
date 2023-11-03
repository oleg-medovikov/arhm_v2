from disp.start import router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot
import asyncio

from func import delete_message, get_chat_fio, add_keyboard
from mdls import MessText, User, Sticker
from call import CallUser


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    """
    начало, тут нужно записать юзера, если он еще не записан
    ну и показать дисклеймер
    """
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None:
        user = await User.create(
            tg_id=message.chat.id, fio=get_chat_fio(message), admin=False
        )

    mess = await MessText.query.where(MessText.name == "disclaimer").gino.first()
    DICT = {
        "Согласиться": CallUser(action="start_new_game", user_id=user.id).pack(),
    }

    sticker = await Sticker.query.where(Sticker.name == "ктулху").gino.first()
    if sticker is not None:
        STICKER = await bot.send_sticker(message.chat.id, sticker=sticker.send_id)

    await asyncio.sleep(3)

    await bot.delete_message(message.chat.id, STICKER.message_id)

    return await message.answer(mess.text, reply_markup=add_keyboard(DICT))
