from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, item_description
from call import CallInventory
from mdls import Item, Sticker


@router.callback_query(CallInventory.filter(F.action == "inventory_show_item"))
async def inventory_show_item(
    callback: CallbackQuery, callback_data: CallInventory, bot: Bot
):
    """
    Данный роутер показывает предмет из сумки и предлагает с ним что-то сделать
    если equip - мы рассматриваем экипированный предмет и предлагаем его снять
    иначе мы рассматривает предмет из сумки и предлагаем его использовать или выкинуть
    """
    item = await Item.get(callback_data.item)
    # проверяем, есть ли стикер с изображением предмета
    if item.stick_id is not None:
        sticker = await Sticker.get(item.stick_id)
        if sticker is not None:
            image = sticker.name
            # await update_sticker(callback.from_user.id, sticker.name, bot)
        else:
            image = None

    DICT = {}

    if callback_data.equip:
        DICT["снять"] = CallInventory(
            action="inventory_remove_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=callback_data.item,
        ).pack()
    else:
        DICT["использовать"] = CallInventory(
            action="inventory_using_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=callback_data.item,
        ).pack()
        DICT["выбросить"] = CallInventory(
            action="inventory_drop_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=callback_data.item,
        ).pack()

    DICT["назад"] = CallInventory(
        action="inventory_main",
        profession=callback_data.profession,
        person_id=callback_data.person_id,
        i_id=callback_data.i_id,
        equip=callback_data.equip,
        item=0,
    ).pack()

    return await update_message(
        bot,
        callback.message,
        item_description(item),
        add_keyboard(DICT),
        image_name=image,
    )
