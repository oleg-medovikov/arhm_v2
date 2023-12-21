from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from random import choices

from mdls import Sticker, Action, Event, Person
from func import (
    update_message,
    add_keyboard,
    update_sticker,
    waste_time,
    check,
    person_change,
)
from call import CallPerson, CallAction


@router.callback_query(CallAction.filter(F.action == "event_start"))
async def event_start(callback: CallbackQuery, callback_data: CallAction, bot: Bot):
    """
    Перед тем как начать ивент, необходимо его выбрать,
    у действия есть список ивентов и список весовых коэффициентов,
    влияющих на частоту выпадания ивента. проверок здесь нет.
    """
    DICT = {}
    # достаем действие и выбираем ивент
    action = await Action.get(callback_data.action_id)
    # тут нужна проверка на single_use проходил ли игрок эти разовые ивенты

    # ===============
    if len(action.events):
        event_id = choices(action.events, weights=action.weights)[0]
    else:
        # если для этого действия нет доступных ивентов
        mess = "тут нечего делать!"
        DICT["понятно"] = CallAction(
            action="action_main",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            loc_id=callback_data.loc_id,
            action_id=0,
        ).pack()
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # Достаем выбранный ивент
    event = await Event.get(event_id)
    if event is None:
        mess = f"несуществующий евент {event_id}"
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # начинаем проходить ивент!
    # при надобности меняем стикер
    if event.stick_id:
        sticker = await Sticker.get(event.stick_id)
        await update_sticker(callback.from_user.id, sticker.name, bot)

    person = await Person.get(callback_data.person_id)
    if event.waste_time:
        # тратим время
        person = await waste_time(person, event.waste_time)
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
    if "choice" not in event.demand:
        # если ивент с проверками, но без выбора вариантов
        mess = event.description
        sucsess = None
        for dict_ in check(person, event.demand):
            mess += dict_.get("mess", "")
            sucsess = dict_["sucsess"]
            if sucsess is False:
                break

        if sucsess is True:
            mess += "\n\n" + event.mess_prise
            await person_change(person, event.prise)
        elif sucsess is False:
            mess += "\n\n" + event.mess_punish
            await person_change(person, event.punish)
        DICT = {
            "продолжить": CallAction(
                action="action_main",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                loc_id=callback_data.loc_id,
                action_id=0,
            ).pack()
        }
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # if 'choice' not in event.demand:
    # тут нужно поставить условие, что игрок в состоянии прохождения ивента
