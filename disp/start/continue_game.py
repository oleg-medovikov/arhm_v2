from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker, person_status_card
from mdls import Person
from call import CallPerson


@router.callback_query(CallPerson.filter(F.action == "continue_game"))
async def continue_game(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    person = await Person.get(callback_data.person_id)

    mess = person_status_card(person)

    DICT = {"Подготовка": CallPerson(action="prep_main", person_id=person.id).pack()}

    await update_sticker(callback.from_user.id, None, bot)
    return await update_message(callback.message, mess, add_keyboard(DICT))
