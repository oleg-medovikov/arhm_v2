from disp.excel import router
from aiogram import F, Bot
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from func import delete_message, add_keyboard
from mdls import User, Sticker
from call import CallSticker


@router.message(F.content_type.in_(["sticker"]))
async def get_sticker_id(message: Message, bot: Bot):
    "посмотреть идентификатор стикера и добавить его в базу"
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if (
        user is None
        or not user.admin
        or message.sticker is None
        or message.sticker.thumbnail is None
    ):
        return

    file_id = message.sticker.file_id
    f_unique_id = message.sticker.thumbnail.file_unique_id

    # проверяем наличие стикера в базе
    sticker = await Sticker.query.where(Sticker.unique_id == f_unique_id).gino.first()
    if sticker is not None:
        mess = f"Данный стикер уже есть в базе\nid: {sticker.id}\nname: {sticker.name}"
        await message.answer(
            mess.replace("_", "\\_"), disable_notification=True, parse_mode="Markdown"
        )
        return bot.send_sticker(message.chat.id, sticker=file_id)

    # если стикера нет в базе, то закидываем его в базу
    # и спрашиваем название у пользователя
    sticker = await Sticker.create(
        name="", category="", unique_id=f_unique_id, send_id=file_id, u_id=user.id
    )

    mess = f"я принял стикер! его id: \n {sticker.id}".replace("_", "\\_")

    DICT = {
        "добавить название": CallSticker(
            action="ask_name", sticker_id=sticker.id
        ).pack()
    }

    # await bot.send_sticker(message.chat.id, sticker=file_id)
    return await message.answer(
        mess,
        reply_markup=add_keyboard(DICT),
    )
