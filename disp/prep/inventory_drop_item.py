from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F


from func import update_message, add_keyboard
from call import CallInventory
from mdls import Person, Item, Inventory, MessText, ItemDrop


@router.callback_query(CallInventory.filter(F.action == "inventory_drop_item"))
async def inventory_drop_item(callback: CallbackQuery, callback_data: CallInventory):
    """
    Персонаж оставляет предмет на локации.
    предлагается оставить записку вместе с предметом,
    может ли нашедший этот предмет забрать его как подарок
    или должен оставить на месте.
    это взаимодействие между игроками
    """

    item = await Item.get(callback_data.item)

    DICT = {
        "подарить нашедшему": CallInventory(
            action="inventory_drop_item_good",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=item.id,
        ).pack(),
        "попросить не трогать": CallInventory(
            action="inventory_drop_item_bad",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=item.id,
        ).pack(),
        "назад": CallInventory(
            action="inventory_show_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=item.id,
        ).pack(),
    }
    return await update_message(callback.message, item.mess_drop, add_keyboard(DICT))


@router.callback_query(
    CallInventory.filter(
        F.action in ("inventory_drop_item_good", "inventory_drop_item_bad")
    )
)
async def inventory_drop_item_end(
    callback: CallbackQuery, callback_data: CallInventory
):
    """
    выкинуть предмет можно только из сумки
    """
    inventory = await Inventory.get(callback_data.i_id)
    inventory.bag.remove(callback_data.item)
    await inventory.update(bag=inventory.bag).apply()

    if callback_data.action == "inventory_drop_item_good":
        mess = await MessText.get(f"item_drop_{callback_data.profession}_good")
    else:
        mess = await MessText.get(f"item_drop_{callback_data.profession}_bad")

    person = await Person.get(callback_data.person_id)
    await ItemDrop.create(
        i_id=callback_data.item,
        l_id=person.loc_id,
        p_id=person.id,
        gift=True if callback_data.action == "inventory_drop_item_good" else False,
    )

    DICT = {
        "назад": CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=callback_data.item,
        ).pack()
    }
    return await update_message(callback.message, mess.text, add_keyboard(DICT))
