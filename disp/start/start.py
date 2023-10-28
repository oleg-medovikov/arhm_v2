from aiogram.types import Message
from aiogram.filters import CommandStart

from disp import dp
from func import delete_message, get_chat_fio, add_keyboard
from mdls import MessText, User


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None:
        await User.create(tg_id=message.chat.id, fio=get_chat_fio(message), admin=False)

    mess = await MessText.query.where(MessText.name == "disclaimer").gino.first()
    DICT = {
        "Согласиться": "start_new_game",
    }
    keyboard = add_keyboard(DICT)
    return await message.answer(mess.text, reply_markup=keyboard)
