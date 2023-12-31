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
    # распаковываем калбек
    data = callback_data.unpack_person()
    # неплохо тут сделать проверку, живой ли персонаж
    person = await Person.get(data["id"])

    # тут делаем проверку на наличие незаконченных действий
    action = (
        await ActionLog.load(person=Person)
        .query.where(and_(ActionLog.person == data["id"], ActionLog.finish == false()))
        .gino.first()
    )
    if action is not None:
        if action.e_id:
            mess = "У Вас незаконченное событие!"
            DICT = {
                "Понятно": CallAny(
                    action="event_start",
                    person=person.param_to_str(),
                    meta=CallAny.pack_meta(
                        {"action_id": action.a_id, "event_id": action.e_id}
                    ),
                ).pack(),
            }
            return await update_message(
                bot, callback.message, mess, add_keyboard(DICT), image_name="ктулху"
            )
    # ===============================================

    mess = person_status_card(person)

    DICT = {
        "Дневник": CallAny(
            action="prep_main", person=person.param_to_str(), meta=""
        ).pack(),
        "Сумка": CallAny(
            action="inventory_main",
            person=person.param_to_str(),
            meta=CallAny.pack_meta({"equip": False, "item": 0}),
        ).pack(),
        "Действие": CallAny(
            action="action_main",
            person=person.param_to_str(),
            meta=CallAny.pack_meta({"action_id": 0, "event": 0}),
        ).pack(),
    }

    return await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT),
        image_user=person.avatar,
        image_name=person.profession,
    )
