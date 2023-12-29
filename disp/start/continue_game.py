from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_, false


from func import update_message, add_keyboard, person_status_card
from mdls import Person, ActionLog
from call import CallPerson, CallInventory, CallAction


@router.callback_query(CallPerson.filter(F.action == "continue_game"))
async def continue_game(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    person = await Person.get(callback_data.person_id)
    # неплохо тут сделать проверку, живой ли персонаж

    # тут делаем проверку на наличие незаконченных действий
    action = (
        await ActionLog.load(person=Person)
        .query.where(
            and_(
                ActionLog.person == callback_data.person_id, ActionLog.finish == false()
            )
        )
        .gino.first()
    )
    if action is not None:
        if action.e_id:
            mess = "У Вас незаконченное событие!"
            DICT = {
                "Понятно": CallAction(
                    action="event_start",
                    person_id=person.id,
                    profession=person.profession,
                    loc_id=person.loc_id,
                    action_id=action.a_id,
                    event=action.e_id,
                ).pack(),
            }
            return await update_message(
                bot, callback.message, mess, add_keyboard(DICT), image_name="ктулху"
            )
    # ===============================================

    mess = person_status_card(person)

    DICT = {
        "Дневник": CallPerson(
            action="prep_main",
            person_id=person.id,
            profession=person.profession,
            i_id=person.i_id,
        ).pack(),
        "Сумка": CallInventory(
            action="inventory_main",
            profession=person.profession,
            person_id=person.id,
            i_id=person.i_id,
            equip=False,
            item=0,
        ).pack(),
        "Действие": CallAction(
            action="action_main",
            person_id=person.id,
            profession=person.profession,
            loc_id=person.loc_id,
            action_id=0,
            event=0,
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
