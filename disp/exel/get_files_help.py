from aiogram.types import Message
from aiogram.filters import Command

from disp import dp
from func import delete_message
from mdls import User

MESS = """*Доступные команды для редактирования базы:*

    /MessText
    /Location

""".replace(
    "_", "\\_"
)


@dp.message(Command("files"))
async def get_files_help(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    return await message.answer(MESS, disable_notification=True, parse_mode="Markdown")
