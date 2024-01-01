from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, item_description
from call import CallAny
from mdls import Item, Image


@router.callback_query(CallAny.filter(F.action == "inventory_show_item"))
async def inventory_show_item(
    callback: CallbackQuery, callback_data: CallAny, bot: Bot
):
    """
    Данный роутер показывает предмет из сумки и предлагает с ним что-то сделать
    если equip - мы рассматриваем экипированный предмет и предлагаем его снять
    иначе мы рассматривает предмет из сумки и предлагаем его использовать или выкинуть
    """
    item = await Item.get(callback_data.item_id)
    # проверяем, есть ли стикер с изображением предмета
    image = None
    if item.image_id:
        image = await Image.get(item.image_id)
        if image is not None:
            image = image.name

    DICT = {}

    if callback_data.equip:
        callback_data.action = "inventory_remove_item"
        DICT["снять"] = callback_data.pack()
    else:
        callback_data.action = "inventory_using_item"
        DICT["использовать"] = callback_data.pack()

        callback_data.action = "inventory_drop_item"
        DICT["выбросить"] = callback_data.pack()

    callback_data.action = "inventory_main"
    callback_data.item_id = 0

    DICT["назад"] = callback_data.pack()

    return await update_message(
        bot,
        callback.message,
        item_description(item),
        add_keyboard(DICT),
        image_name=image,
    )
