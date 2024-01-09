from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from mdls import Image
from func import update_message, add_keyboard, inventory_show
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "inventory_main"))
async def inventory_main(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    Данный роутер сразу 2 функции выполняет. просмотр инвентаря с сумкой и с экипированными вещами
    """
    mess, items = await inventory_show(callback_data.inventory_id, callback_data.equip)

    DICT = {}
    # список кнопок с предметами
    callback_data.action = "inventory_show_item"
    for key, value in items.items():
        callback_data.item_id = key
        DICT[value] = callback_data.pack()

    if callback_data.equip:
        # картинка инвентори
        image = await Image.query.where(Image.name == "инвентарь").gino.first()
        if image:
            image = image.name
        # вернуться к просмотру сумки
        callback_data.action = "inventory_main"
        callback_data.equip = False
        callback_data.item_id = 0

        DICT["назад"] = callback_data.pack()
    else:
        # картинка сумки
        image = await Image.query.where(Image.name == "сумка").gino.first()
        if image:
            image = image.name
        # кнопка посмотреть экипированные предметы
        callback_data.action = "inventory_main"
        callback_data.equip = True
        callback_data.item_id = 0

        DICT["экипированные вещи"] = callback_data.pack()

        # кнопка возврата в prep_main
        callback_data.action = "continue_game"

        DICT["назад"] = callback_data.pack()

    await update_message(
        bot, callback.message, mess, add_keyboard(DICT), image_name=image
    )
