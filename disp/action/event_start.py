from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_
from random import choices

from mdls import Sticker, Action, Event
from func import update_message, add_keyboard, update_sticker, demand
from call import CallPerson, CallAction


@router.callback_query(CallAction.filter(F.action == "event_start"))
async def action_main(callback: CallbackQuery, callback_data: CallAction, bot: Bot):
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
        await update_sticker(callback.from_user.id, .sticker.name, bot)
    
    if len(event.demand) == 0:
        # это пассивный эвент, просто отправляем описание и кнопку вернуться
        # тратим время
        

    # тут нужно поставить условие, что игрок в состоянии прохождения ивента
    
    # стикер с изображением локации
    locd = (
        await LocDescription.load(location=Location, sticker=Sticker)
        .query.where(
            and_(
                LocDescription.loc_id == callback_data.loc_id,
                LocDescription.profession == callback_data.profession,
            )
        )
        .gino.first()
    )
