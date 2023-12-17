from disp.start import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker, person_status_card
from mdls import Person
from call import CallPerson, CallInventory, CallAction


@router.callback_query(CallPerson.filter(F.action == "continue_game"))
async def continue_game(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    person = await Person.get(callback_data.person_id)

    # неплохо тут сделать проверку, живой ли персонаж

    # ===============================================

    mess = person_status_card(person)

    DICT = {
        "Дневник": CallPerson(
            action="prep_main",
            person_id=person.id,
            profession=person.profession,
            i_id=person.i_id,
        ).pack(),
        "Сумка": CallInventory(
            action="inventory_main",
            profession=person.profession,
            person_id=person.id,
            i_id=person.i_id,
            equip=False,
            item=0,
        ).pack(),
        "Действие": CallAction(
            action="action_main",
            person_id=person.id,
            profession=person.profession,
        ).pack(),
    }

    await update_message(callback.message, mess, add_keyboard(DICT))
    return await update_sticker(callback.from_user.id, None, bot)
