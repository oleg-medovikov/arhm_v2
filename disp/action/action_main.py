from disp.action import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot
from sqlalchemy import and_


from mdls import LocDescription, Location, Sticker
from func import update_message, add_keyboard, update_sticker
from call import CallPerson, CallAction


@router.callback_query(CallAction.filter(F.action == "action_main"))
async def action_main(callback: CallbackQuery, callback_data: CallAction, bot: Bot):
    """
    здесь мы показываем игроку описание локации, в которой он находится
    и показываем все доступные кнопки действий
    конечно, необходимо проверить, проходит ли игрок требования
    """
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
    await update_sticker(callback.from_user.id, locd.sticker.name, bot)
    # теперь описание локации
    mess = f"*Локация: {locd.location.name}* \n\n{locd.description}"
    DICT = {}

    DICT["назад"] = CallPerson(
        action="continue_game",
        person_id=callback_data.person_id,
        profession=callback_data.profession,
        i_id=0,
    ).pack()

    await update_message(callback.message, mess, add_keyboard(DICT))
