from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_, false

from func import add_keyboard, update_message

from mdls import Person, MessText
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "start_new_game"))
async def start_new_game(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    Если есть живой персонаж, говорим, что уже видели игрока, предлагаем
    продолжить игру или прочесть правила.
    Если нет живого персонажа, встречаем запугиванием и заставляем пройти анкету.

    """
    # распаковываем id юзера из меты
    user_id = callback_data.user_id

    person = await Person.query.where(
        and_(Person.u_id == user_id, Person.death == false())
    ).gino.first()

    if person is None:
        mess = await MessText.get("hello_no_person")
        call = callback_data
        call.action = "register"

        DICT = {"регистрация у шерифа": call.pack()}
        return await update_message(
            bot, callback.message, mess.text, add_keyboard(DICT)
        )

    mess = await MessText.get("hello_exist_person")
    call = callback_data
    call.action = "continue_game"
    call.person_id = person.id

    DICT = {"продолжить игру": call.pack()}
    return await update_message(bot, callback.message, mess.text, add_keyboard(DICT))
