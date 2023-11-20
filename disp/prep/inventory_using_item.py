from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F


from func import update_message, add_keyboard, item_using
from call import CallInventory
from mdls import Person, Item, Inventory


@router.callback_query(CallInventory.filter(F.action == "inventory_using_item"))
async def inventory_using_item(callback: CallbackQuery, callback_data: CallInventory):
    """
    Использование предмета. Это в зависимости от предмета
    надеть его или использовать ради эффекта
    """

    item = await Item.get(callback_data.item)
    person = await Person.get(callback_data.person_id)
    inventory = await Inventory.get(callback_data.i_id)

    check, mess = await item_using(person, inventory, item)
    if check:
        mess = "* Удачно! * \n" + mess
    else:
        mess = "* Неудача! * \n" + mess

    DICT = {}
    DICT["назад"] = CallInventory(
        action="inventory_main",
        profession=callback_data.profession,
        person_id=callback_data.person_id,
        i_id=callback_data.i_id,
        equip=callback_data.equip,
        item=item.id,
    ).pack()

    await update_message(callback.message, mess, add_keyboard(DICT))
