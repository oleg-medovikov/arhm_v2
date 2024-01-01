from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard
from call import CallAny
from mdls import Person, Item, Inventory, MessText, ItemDrop


@router.callback_query(CallAny.filter(F.action == "inventory_drop_item"))
async def inventory_drop_item(
    callback: CallbackQuery, callback_data: CallAny, bot: Bot
):
    """
    Персонаж оставляет предмет на локации.
    предлагается оставить записку вместе с предметом,
    может ли нашедший этот предмет забрать его как подарок
    или должен оставить на месте.
    это взаимодействие между игроками
    """

    item = await Item.get(callback_data.item_id)

    callback_data.action = "inventory_show_item"
    call_back = callback_data.pack()

    callback_data.action = "inventory_drop_item_end"
    callback_data.equip = True
    call_present = callback_data.pack()

    callback_data.equip = False
    call_no_present = callback_data.pack()

    DICT = {
        "подарить нашедшему": call_present,
        "попросить не трогать": call_no_present,
        "назад": call_back,
    }
    return await update_message(
        bot, callback.message, item.mess_drop, add_keyboard(DICT)
    )


@router.callback_query(CallAny.filter(F.action == "inventory_drop_item_end"))
async def inventory_drop_item_end(
    callback: CallbackQuery, callback_data: CallAny, bot: Bot
):
    """
    выкинуть предмет можно только из сумки
    """
    person = await Person.get(callback_data.person_id)
    inventory = await Inventory.get(callback_data.inventory_id)
    inventory.bag.remove(callback_data.item_id)
    await inventory.update(bag=inventory.bag).apply()

    if callback_data.equip:
        mess = await MessText.get(f"item_drop_{person.profession}_good")
    else:
        mess = await MessText.get(f"item_drop_{person.profession}_bad")

    person = await Person.get(callback_data.person_id)
    await ItemDrop.create(
        i_id=callback_data.item_id,
        l_id=person.loc_id,
        p_id=person.id,
        gift=callback_data.equip,
    )

    callback_data.action = "inventory_main"
    callback_data.equip = False
    call_back = callback_data.pack()

    DICT = {"назад": call_back}
    return await update_message(bot, callback.message, mess.text, add_keyboard(DICT))
