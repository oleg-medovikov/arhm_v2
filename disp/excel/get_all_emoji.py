from disp.excel import router
from aiogram.types import Message
from aiogram.filters import Command

from func import delete_message
from mdls import User
from conf import emoji_all, emoji


@router.message(Command("get_emoji"))
async def get_all_emoji(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    MAX_LEN = max((len(k) for k in emoji_all()))
    MESS = ""
    for key in emoji_all():
        word = key + " " * (MAX_LEN - len(key))
        MESS += f" { word }   " + emoji(key) + "\n"

    MESS = f"` \n{MESS} `"

    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
