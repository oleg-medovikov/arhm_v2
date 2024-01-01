from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_, false

from func import update_message, add_keyboard, person_status_card
from mdls import Person, ActionLog

# from call import CallPerson, CallInventory, CallAction
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "continue_game"))
async def continue_game(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    # неплохо тут сделать проверку, живой ли персонаж
    person = await Person.get(callback_data.person_id)

    # тут делаем проверку на наличие незаконченных действий
    action = (
        await ActionLog.load(person=Person)
        .query.where(and_(ActionLog.person == person.id, ActionLog.finish == false()))
        .gino.first()
    )
    if action is not None:
        if action.e_id:
            mess = "У Вас незаконченное событие!"
            call_event = callback_data
            call_event.action = "event_start"
            call_event.action_id = action.id
            call_event.event_id = action.e_id

            DICT = {"Понятно": call_event.pack()}
            return await update_message(
                bot, callback.message, mess, add_keyboard(DICT), image_name="ктулху"
            )
    # ===============================================

    mess = person_status_card(person)

    call_dnevnic = callback_data
    call_dnevnic.action = "prep_main"

    call_bag = callback_data
    call_bag.action = "inventory_main"

    call_action = callback_data
    call_action.action = "action_main"

    DICT = {
        "Дневник": call_dnevnic.pack(),
        "Сумка": call_bag.pack(),
        "Действие": call_action.pack(),
    }

    return await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT),
        image_user=person.avatar,
        image_name=person.profession,
    )
