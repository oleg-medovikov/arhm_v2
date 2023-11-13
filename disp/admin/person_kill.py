from disp.admin import router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import and_, false
from datetime import datetime

from func import delete_message
from mdls import User, Person


@router.message(Command("kill"))
async def person_kill(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    person = await Person.query.where(
        and_(Person.u_id == user.id, Person.death == false())
    ).gino.first()
    if person is None:
        mess = "у Вас нет живых персонажей"
        return await message.answer(
            mess, disable_notification=True, parse_mode="Markdown"
        )

    await person.update(
        death=True, death_reason="Убит по команде", death_date=datetime.now()
    ).apply()
    mess = "я убил вашего персонажа"
    return await message.answer(mess, disable_notification=True, parse_mode="Markdown")
