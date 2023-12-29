from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard
from mdls import MessText
from call import CallPerson, CallNotes


@router.callback_query(CallPerson.filter(F.action == "prep_main"))
async def prep_main(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    mess = await MessText.get(f"prep_main_{callback_data.profession}")
    # await update_sticker(callback.from_user.id, "студентка", bot)

    DICT = {
        "записи в дневнике": CallNotes(
            action="read_notes",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
            gametime=-1,
        ).pack(),
        "ваша фотокарточка": CallPerson(
            action="avatar_main",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
        ).pack(),
        # "карта": "map",
        "назад": CallPerson(
            action="continue_game",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
        ).pack(),
    }
    await update_message(
        bot, callback.message, mess.text, add_keyboard(DICT), image_name="дневник"
    )
