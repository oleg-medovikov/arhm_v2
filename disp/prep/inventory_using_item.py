from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker
from call import CallInventory
from mdls import Item, Sticker


@router.callback_query(CallInventory.filter(F.action == "inventory_show_item"))
async def inventory_eqiup_item(
    callback: CallbackQuery, callback_data: CallInventory, bot: Bot
):
 
