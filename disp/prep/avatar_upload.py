from disp.prep import router
from aiogram.types import CallbackQuery, Message
from aiogram import F, Bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from func import update_message, add_keyboard
from mdls import User, UserImage
from call import CallAny


# Определение состояний FSM
class PhotoStates(StatesGroup):
    waiting_for_photo = State()


@router.callback_query(CallAny.filter(F.action == "avatar_upload"))
async def avatar_upload(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    спрашиваем загрузить фотографию
    """

    # Обработчик загрузки фото


@router.message(F.content_type.in_(["photo"]), state=PhotoStates.waiting_for_photo)
async def handle_photo(message: Message, state: FSMContext, bot: Bot):
    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    # Получаем объект photo
    if not message.photo:
        return
    photo = message.photo[-1]
    # Получаем файл объекта photo
    file = await bot.get_file(photo.file_id)
    print(file)
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
    image = await UserImage.create(
        name=photo.filename.,
        category="",
        file_id=photo.file_id,
        file=binary_data,
        u_id=user.id,
    )

    await state.finish()
