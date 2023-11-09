from disp.start import router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot


from func import delete_message, get_chat_fio, add_keyboard, update_sticker
from mdls import MessText, User
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

    await update_sticker(message.chat.id, "ктулху", bot)

    return await message.answer(mess.text, reply_markup=add_keyboard(DICT))
