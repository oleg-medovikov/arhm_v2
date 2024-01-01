from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard
from mdls import MessText
from call import CallAny
from mdls import Person


@router.callback_query(CallAny.filter(F.action == "prep_main"))
async def prep_main(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    person = await Person.get(callback_data.person_id)
    mess = await MessText.get(f"prep_main_{person.profession}")

    # чтонеие заметок
    callback_data.action = "read_notes"
    callback_data.gametime = -1
    call_notes = callback_data.pack()
    # смена картинки аватара
    callback_data.action = "avatar_main"
    call_foto = callback_data.pack()
    # назад
    callback_data.action = "continue_game"
    call_back = callback_data.pack()

    DICT = {
        "записи в дневнике": call_notes,
        "ваша фотокарточка": call_foto,
        # "карта": "map",
        "назад": call_back,
    }
    await update_message(
        bot, callback.message, mess.text, add_keyboard(DICT), image_name="дневник"
    )
