from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker
from mdls import Person, MessText
from call import CallPerson


@router.callback_query(CallPerson.filter(F.action == "prep_main"))
async def prep_main(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    person = await Person.get(callback_data.person_id)

    mess = await MessText.get(f"prep_main_{person.profession}")
    await update_sticker(callback.from_user.id, "студентка", bot)

    DICT = {"назад": CallPerson(action="continue_game", person_id=person.id).pack()}
    await update_message(callback.message, mess.text, add_keyboard(DICT))
