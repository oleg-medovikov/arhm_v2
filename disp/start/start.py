from disp.start import router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Bot


from func import (
    get_chat_fio,
    add_keyboard,
    update_message,
)
from mdls import MessText, User
from call import CallAny


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot):
    """
    начало, тут нужно записать юзера, если он еще не записан
    ну и показать дисклеймер
    """

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None:
        user = await User.create(
            tg_id=message.chat.id, fio=get_chat_fio(message), admin=False
        )

    mess = await MessText.query.where(MessText.name == "disclaimer").gino.first()
    DICT = {
        "Согласиться": CallAny(
            action="start_new_game",
            person="",
            meta=CallAny.pack_meta({"user_id": user.id}),
        ).pack(),
    }

    return await update_message(
        bot, message, mess.text, add_keyboard(DICT), image_name="ктулху"
    )
