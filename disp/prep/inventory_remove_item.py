from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F


from func import update_message, add_keyboard, item_remove
from call import CallInventory
from mdls import Person, Item, Inventory


@router.callback_query(CallInventory.filter(F.action == "inventory_remove_item"))
async def inventory_remove_item(callback: CallbackQuery, callback_data: CallInventory):
    """
    Снятие предмета с тела.
    перемещение в сумку и убирание эффектов
    """

    person = await Person.get(callback_data.person_id)
    inventory = await Inventory.get(callback_data.i_id)
    item = await Item.get(callback_data.item)

    check, mess, DICT = await item_remove(person, inventory, item)

    # если не удалось снять, возвращаемся в экипированные предметы
    if not check:
        DICT["назад"] = CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=True,
            item=item.id,
        ).pack()
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # если удалось снять без условий, возвращаемся в просмотр сумки
    if check and len(DICT) == 0:
        DICT["назад"] = CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=False,
            item=item.id,
        ).pack()
        return await update_message(callback.message, mess, add_keyboard(DICT))

    # если есть выбор альтернативных предметов - создаем кнопки на using_item
    dict_ = {}
    for key, value in DICT.items():
        dict_[value] = CallInventory(
            action="inventory_using_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=key,
        ).pack()
    return await update_message(callback.message, mess, add_keyboard(dict_))
