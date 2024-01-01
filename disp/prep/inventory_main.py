from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, update_sticker, inventory_show
from call import CallAny, CallPerson, CallInventory


@router.callback_query(CallAny.filter(F.action == "inventory_main"))
async def inventory_main(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    Данный роутер сразу 2 функции выполняет. просмотр инвентаря с сумкой и с экипированными вещами
    """
    mess, items = await inventory_show(callback_data.inventory_id, callback_data.equip)
    """
    DICT = {}
    # список кнопок с предметами
    for key, value in items.items():
        DICT[value] = CallInventory(
            action="inventory_show_item",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=callback_data.equip,
            item=key,
        ).pack()

    if callback_data.equip:
        # вернуться к просмотру сумки
        DICT["назад"] = CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=False,
            item=0,
        ).pack()
    else:
        # кнопка посмотреть экипированные предметы
        DICT["экипированные вещи"] = CallInventory(
            action="inventory_main",
            profession=callback_data.profession,
            person_id=callback_data.person_id,
            i_id=callback_data.i_id,
            equip=True,
            item=0,
        ).pack()
        # кнопка возврата в prep_main
        DICT["назад"] = CallPerson(
            action="continue_game",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
        ).pack()

    await update_message(
        bot, callback.message, mess, add_keyboard(DICT), image_name="дневник"
    )
    """

    print("!!!! TEST")
