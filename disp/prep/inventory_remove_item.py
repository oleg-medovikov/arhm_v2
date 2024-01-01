from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, item_remove
from call import CallAny
from mdls import Person, Item, Inventory


@router.callback_query(CallAny.filter(F.action == "inventory_remove_item"))
async def inventory_remove_item(
    callback: CallbackQuery, callback_data: CallAny, bot: Bot
):
    """
    Снятие предмета с тела.
    перемещение в сумку и убирание эффектов
    """

    person = await Person.get(callback_data.person_id)
    inventory = await Inventory.get(callback_data.inventory_id)
    item = await Item.get(callback_data.item_id)

    check, mess, DICT = await item_remove(person, inventory, item)

    # если не удалось снять, возвращаемся в экипированные предметы
    if not check:
        callback_data.action = "inventory_main"
        callback_data.equip = True
        DICT["назад"] = callback_data.pack()
        return await update_message(bot, callback.message, mess, add_keyboard(DICT))

    # если удалось снять без условий, возвращаемся в просмотр сумки
    if check and len(DICT) == 0:
        callback_data.action = "inventory_main"
        callback_data.equip = False
        DICT["назад"] = callback_data.pack()
        return await update_message(bot, callback.message, mess, add_keyboard(DICT))

    # если есть выбор альтернативных предметов - создаем кнопки на using_item
    dict_ = {}
    for key, value in DICT.items():
        callback_data.action = "inventory_using_item"
        callback_data.item_id = key

        dict_[value] = callback_data.pack()
    return await update_message(bot, callback.message, mess, add_keyboard(dict_))
