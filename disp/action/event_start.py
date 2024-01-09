from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from random import choices

from conf import emoji
from mdls import Image, Action, Event, Person, ActionLog
from func import (
    update_message,
    add_keyboard,
    waste_time,
    check,
    person_change,
    timedelta_to_str,
)
from call import CallAny, CallAction, CallEvent


@router.callback_query(CallAny.filter(F.action == "event_start"))
async def event_start(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    Перед тем как начать ивент, необходимо его выбрать,
    у действия есть список ивентов и список весовых коэффициентов,
    влияющих на частоту выпадания ивента. проверок здесь нет.
    Если ивент в каллэкшене не равен нулю - значит, персонаж уже
    в состоянии прохождения ивента!
    """
    DICT = {}
    # достаем действие и выбираем ивент
    action = await Action.get(callback_data.action_id)
    if callback_data.event_id != 0:
        event_id = callback_data.event_id
    elif len(action.events):
        event_id = choices(action.events, weights=action.weights)[0]
        # тут нужна проверка на single_use проходил ли игрок эти разовые ивенты

        # ===============
    else:
        # если для этого действия нет доступных ивентов
        mess = "тут нечего делать!"
        callback_data.action = "action_main"
        callback_data.action_id = 0
        callback_data.event_id = 0
        DICT["понятно"] = callback_data.pack()
        return await update_message(bot, callback.message, mess, add_keyboard(DICT))

    # Достаем выбранный ивент
    event = await Event.get(event_id)
    if event is None:
        # это какая-то ошибка, не должно такого быть!
        mess = f"!!! несуществующий евент {event_id}"
        callback_data.action = "action_main"
        callback_data.action_id = 0
        callback_data.event_id = 0
        DICT["понятно"] = callback_data.pack()
        return await update_message(bot, callback.message, mess, add_keyboard(DICT))

    # начинаем проходить ивент!
    # при надобности меняем картинку
    if event.image_id:
        image = await Image.get(event.image_id)
    else:
        image = None

    if "choice" not in event.demand:
        # тратим время
        person = await Person.get(callback_data.person_id)
        event_time = person.gametime
        person = await waste_time(person, event.waste_time)
        event_time = person.gametime - event_time
        # добавить сюда подарок и наказание, если они не пустые (не обязательно)
        if person.death:
            # Если персонаж внезапно умер
            mess = "похоже случилось непоправимое"
            callback_data.action = "continue_game"

            DICT = {"...": callback_data.pack()}
            return await update_message(
                bot, callback.message, mess, add_keyboard(DICT), image_name=image
            )
        # если ивент с проверками, но без выбора вариантов
        # делается в одно сообщение
        mess = (
            emoji("clock")
            + " "
            + timedelta_to_str(event_time)
            + "\n\n"
            + event.description
        )
        sucsess = None
        for dict_ in check(person, event.demand):
            mess += dict_.get("mess", "")
            sucsess = dict_["sucsess"]
            if sucsess is False:
                break
        location = person.loc_id
        if sucsess is True:
            mess += "\n\n" + event.mess_prise
            person = await person_change(person, event.prise)
        elif sucsess is False:
            mess += "\n\n" + event.mess_punish
            person = await person_change(person, event.punish)

        # создать лог по прохождению события
        await ActionLog.create(
            p_id=person.id,
            gametime=person.gametime,
            a_id=callback_data.action_id,
            finish=True,
            e_id=event.id,
            check=sucsess,
            loc_start=location,
            loc_finish=person.loc_id,
        )
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

    if "choice" in event.demand:
        # создать лог по прохождению события
        if callback_data.event == 0:
            # это первый запуск ивента, а не повторный
            person = await Person.get(callback_data.person_id)
            await ActionLog.create(
                p_id=person.id,
                gametime=person.gametime,
                a_id=callback_data.action_id,
                finish=False,
                e_id=event.id,
                loc_start=person.loc_id,
            )

        for i, key in enumerate(event.demand["choice"]):
            # тут i = 0 это true
            DICT[key] = CallEvent(
                action="event_end",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                loc_id=callback_data.loc_id,
                event_id=event.id,
                choice=False if i else True,
            )

        return await update_message(
            callback.message, event.description, add_keyboard(DICT)
        )
