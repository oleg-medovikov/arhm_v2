from aiogram import F
from aiogram.types import Message

from disp.excel import router
from func import delete_message
from mdls import Image, User


@router.message(F.text.startswith("image"))
async def watch_Image(message: Message):
    "посмотреть картинку по номеру"
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    try:
        number = int(str(message.text).split(" ")[-1])
    except Exception:
        mess = "не нашел номера в сообщении"
        return await message.answer(
            mess, disable_notification=True, parse_mode="Markdown"
        )

    image = await Image.get(number)

    if image is None:
        mess = f"нет картинки с id {number}"
        return await message.answer(
            mess, disable_notification=True, parse_mode="Markdown"
        )

    mess = f"id: {image.id}  " + image.name
    await message.answer_photo(
        photo=image.file_id,
        caption=mess,
        disable_notification=True,
        parse_mode="Markdown",
    )
