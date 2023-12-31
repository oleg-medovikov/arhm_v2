from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_, false
from ast import literal_eval

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
    meta = callback_data.unpack_meta()
    user_id = meta["user_id"]

    person = await Person.query.where(
        and_(Person.u_id == user_id, Person.death == false())
    ).gino.first()

    if person is None:
        mess = await MessText.get("hello_no_person")
        DICT = {
            "регистрация у шерифа": CallAny(
                action="register", person="", meta=callback_data.meta
            ).pack(),
        }
        return await update_message(
            bot, callback.message, mess.text, add_keyboard(DICT)
        )

    mess = await MessText.get("hello_exist_person")
    DICT = {
        "продолжить игру": CallAny(
            action="continue_game", person=person.param_to_str(), meta=""
        ).pack(),
    }
    return await update_message(bot, callback.message, mess.text, add_keyboard(DICT))
