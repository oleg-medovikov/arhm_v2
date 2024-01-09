from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_

from mdls import LocDescription, Location, Image, Action, Person
from func import update_message, add_keyboard, demand
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "action_main"))
async def action_main(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    здесь мы показываем игроку описание локации, в которой он находится
    и показываем все доступные кнопки действий
    конечно, необходимо проверить, проходит ли игрок требования
    """
    # вытаскиваем персону, так как надо проходить требования
    person = await Person.get(callback_data.person_id)
    # достаем описание локации с изображением
    locd = (
        await LocDescription.load(location=Location, image=Image)
        .query.where(
            and_(
                LocDescription.loc_id == person.loc_id,
                LocDescription.profession == person.profession,
            )
        )
        .gino.first()
    )
    # теперь описание локации
    mess = f"*Локация: {locd.location.name}* \n\n{locd.description}"
    # вытаскиваем доступные действия, и проверяем требования к ним
    actions = await Action.query.where(
        and_(Action.loc_id == person.loc_id, Action.profession == person.profession)
    ).gino.all()

    # создаем кнопочки, из тех действий, что проходят по рребованиям
    DICT = {}
    for action in actions:
        if await demand(person, action.demand):
            if action.dialog is None:
                callback_data.action = "event_start"
                callback_data.action_id = action.id
                callback_data.event_id = 0

                DICT[action.name] = callback_data.pack()

    # кнопочка отмены, для выхода
    callback_data.action = "continue_game"
    callback_data.action_id = 0
    callback_data.event_id = 0

    DICT["назад"] = callback_data.pack()

    await update_message(
        bot, callback.message, mess, add_keyboard(DICT), image_name=locd.image.name
    )
