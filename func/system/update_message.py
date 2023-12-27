from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from typing import Optional
from aiogram.types import Message, InlineKeyboardMarkup, message_id
from aiogram.types import BufferedInputFile

from mdls import Image, ImageLog


async def update_message(
    bot,
    message: Optional[Message],
    MESS,
    keyboard: Optional[InlineKeyboardMarkup],
    html: bool = False,
    image_id=None,
) -> Optional["Message"]:
    "изменение сообщения с обработкой исключений"
    if message is None:
        return

    mode = "html" if html else "Markdown"
    # в любом случае удаляем комманду пользователя, так как  она не нужна
    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    except TelegramNotFound:
        pass

    # нужно вытащить номер сообщения от бота к пользователю
    log = await ImageLog.query.where(ImageLog.chat_id == message.chat.id).gino.first()
    if log:
        # если сообщение есть, то нужно его апдейтить
        if image_id:
            image = await Image.get(image_id)
            return await bot.edit_message_media(
                chat_id=log.chat_id,
                message_id=log.message_id,
                media=BufferedInputFile(image.file, filename=image.name + ".png"),
                caption=MESS,
                reply_markup=keyboard,
                parse_mode=mode,
            )
        else:
            await bot.edit_message_text(
                chat_id=log.chat_id,
                message_id=log.message_id,
                text=MESS,
            )
            await bot.edit_reply_markup(
                chat_id=log.chat_id, message_id=log.message_id, reply_markup=keyboard
            )
            return message

    # если нет логов, то нужно отправить новое сообщение и записать его в логи
    if image_id:
        image = await Image.get(image_id)
        message = await message.answer_photo(
            BufferedInputFile(image.file, filename=image.name + ".png"),
            caption=MESS,
            reply_markup=keyboard,
            parse_mode=mode,
        )
        await ImageLog.create(
            chat_id=message.chat.id, message_id=message.message_id, name=image.name
        )
        return message

    # вариант без картинки
    message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)
    await ImageLog.create(chat_id=message.chat.id, message_id=message.message_id)
    return message
