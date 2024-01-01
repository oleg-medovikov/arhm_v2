from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot

from func import update_message, add_keyboard, item_using
from call import CallAny
from mdls import Person, Item, Inventory


@router.callback_query(CallAny.filter(F.action == "inventory_using_item"))
async def inventory_using_item(
    callback: CallbackQuery, callback_data: CallAny, bot: Bot
):
    """
    Использование предмета. Это в зависимости от предмета
    надеть его или использовать ради эффекта
    """

    item = await Item.get(callback_data.item_id)
    person = await Person.get(callback_data.person_id)
    inventory = await Inventory.get(callback_data.inventory_id)

    check, mess = await item_using(person, inventory, item)
    if check:
        mess = "* Удачно! * \n" + mess
    else:
        mess = "* Неудача! * \n" + mess

    DICT = {}
    callback_data.action = "inventory_main"
    DICT["назад"] = callback_data.pack()

    await update_message(bot, callback.message, mess, add_keyboard(DICT))
