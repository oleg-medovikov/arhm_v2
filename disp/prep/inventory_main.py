from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker
from mdls import MessText
from call import CallPerson, CallNotes, CallInventory


@router.callback_query(CallInventory.filter(F.action == "inventory_main"))
async def inventory_main(
    callback: CallbackQuery, callback_data: CallInventory, bot: Bot
):
    mess = await MessText.get(f"prep_main_{callback_data.profession}")
    await update_sticker(callback.from_user.id, "студентка", bot)

    DICT = {
        "записи в дневнике": CallNotes(
            action="read_notes",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
            gametime=-1,
        ).pack(),
        "инвентарь": CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            item=0,
        ).pack(),
        # "карта": "map",
        "назад": CallPerson(
            action="continue_game",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
        ).pack(),
    }
    await update_message(callback.message, mess.text, add_keyboard(DICT))
