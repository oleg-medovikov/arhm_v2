from disp.excel import router
from aiogram import F, Bot
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from func import delete_message, add_keyboard
from mdls import User, Image
from call import CallImage


@router.message(F.content_type.in_(["photo"]))
async def add_Image(message: Message, bot: Bot):
    """
    проверить, есть ли такое изображение в базе и добавить его
    """
    await delete_message(message)

    if not message.photo:
        return

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return

    # Получаем объект photo
    photo = message.photo[-1]
    print(photo)
    # Получаем файл объекта photo
    file = await bot.get_file(photo.file_id)
    # Скачиваем файл
    await bot.download_file(file.file_path, "/tmp/image.png")
    binary_data = open("/tmp/image.png", "rb").read()

    # проверяем наличие картинки в базе
    image = await Image.query.where(Image.file == binary_data).gino.first()
    if image is not None:
        mess = f"Эта картинка уже есть в базе\nid: {image.id}\nname: {image.name}"
        return await message.answer(
            mess.replace("_", "\\_"), disable_notification=True, parse_mode="Markdown"
        )

    # если картинки нет в баз, записываем ее в базу
    # и спрашиваем название у пользователя
    image = await Image.create(
        name="",
        category="",
        file_id=photo.file_id,
        file=binary_data,
        u_id=user.id,
    )

    mess = f"Я запомнил картинку, ее id: \n {image.id}".replace("_", "\\_")

    DICT = {
        "добавить название": CallImage(
            action="ask_name_Image", image_id=image.id
        ).pack()
    }

    return await message.answer(
        mess,
        reply_markup=add_keyboard(DICT),
    )
