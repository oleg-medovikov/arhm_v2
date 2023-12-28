from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_, false

from func import add_keyboard, update_message

from mdls import Person, MessText
from call import CallUser, CallPerson


@router.callback_query(CallUser.filter(F.action == "start_new_game"))
async def start_new_game(callback: CallbackQuery, callback_data: CallUser, bot: Bot):
    """
    Если есть живой персонаж, говорим, что уже видели игрока, предлагаем
    продолжить игру или прочесть правила.
    Если нет живого персонажа, встречаем запугиванием и заставляем пройти анкету.

    """
    user_id = callback_data.user_id

    person = await Person.query.where(
        and_(Person.u_id == user_id, Person.death == false())
    ).gino.first()

    if person is None:
        mess = await MessText.get("hello_no_person")
        DICT = {
            "регистрация у шерифа": CallUser(action="register", user_id=user_id).pack(),
        }
        return await update_message(
            bot, callback.message, mess.text, add_keyboard(DICT)
        )

    mess = await MessText.get("hello_exist_person")
    DICT = {
        "продолжить игру": CallPerson(
            action="continue_game",
            person_id=person.id,
            profession=person.profession,
            i_id=person.i_id,
        ).pack(),
    }
    return await update_message(bot, callback.message, mess.text, add_keyboard(DICT))
