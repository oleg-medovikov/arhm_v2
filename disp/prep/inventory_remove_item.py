from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F


from func import update_message, add_keyboard, item_using
from call import CallInventory
from mdls import Person, Item, Inventory


@router.callback_query(CallInventory.filter(F.action == "inventory_remove_item"))
async def inventory_remove_item(callback: CallbackQuery, callback_data: CallInventory):
    """
    Снятие предмета с тела.
    перемещение в сумку и убирание эффектов
    """
