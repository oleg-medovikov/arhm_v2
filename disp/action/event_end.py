from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F
from sqlalchemy import and_, false

from conf import emoji
from mdls import Event, Person, ActionLog
from func import (
    update_message,
    add_keyboard,
    waste_time,
    person_change,
    timedelta_to_str,
)
from call import CallPerson, CallAction, CallEvent


@router.callback_query(CallAction.filter(F.action == "event_end"))
async def event_end(callback: CallbackQuery, callback_data: CallEvent):
    """
    заканчиваем ивенты с выбором
    первым делом, нужно потратить время и проверить
    не случилось ли чего с персонажем

    """
    event = await Event.get(callback_data.event)
    # тратим время
    person = await Person.get(callback_data.person_id)
    event_time = person.gametime
    person = await waste_time(person, event.waste_time)
    event_time = person.gametime - event_time
    # добавить сюда подарок и наказание, если они не пустые (не обязательно)
    if person.death:
        # Если персонаж внезапно умер
        mess = "похоже случилось непоправимое"
        DICT = {
            "...": CallPerson(
                action="continue_game",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                i_id=0,
            ).pack()
        }
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # составляем сообщение
    mess = (
        emoji("clock") + " " + timedelta_to_str(event_time) + "\n\n" + event.description
    )

    if callback_data.choice:
        mess += "\n\n" + event.mess_prise
        person = await person_change(person, event.prise)
    else:
        mess += "\n\n" + event.mess_punish
        person = await person_change(person, event.punish)

    # создать лог по прохождению события
    action = (
        await ActionLog.load(person=Person)
        .query.where(
            and_(
                ActionLog.person == callback_data.person_id, ActionLog.finish == false()
            )
        )
        .gino.first()
    )

    await action.update(
        finish=True,
        e_id=event.id,
        check=callback_data.choice,
        loc_finish=person.loc_id,
    )
    DICT = {
        "продолжить": CallAction(
            action="action_main",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            loc_id=person.loc_id,
            action_id=0,
            event=0,
        ).pack()
    }
    return await update_message(callback.message, mess, add_keyboard(DICT))
