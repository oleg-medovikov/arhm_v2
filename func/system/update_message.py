from typing import Optional
from aiogram.types import InputMediaPhoto, Message, InlineKeyboardMarkup
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods.edit_message_media import EditMessageMedia
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound

from aiogram import Bot

from mdls import Image, ImageLog


async def update_message(
    bot: Bot,
    message: Optional[Message],
    MESS: str,
    keyboard: Optional[InlineKeyboardMarkup],
    html: bool = False,
    image_id: Optional[int] = None,
    image_name: Optional[str] = None,
):
    "изменение сообщения с обработкой исключений"
    if message is None:
        return

    mode = "html" if html else "Markdown"

    # ищем логи сообщений
    log = await ImageLog.query.where(ImageLog.chat_id == message.chat.id).gino.first()
    # ищем картинку в базе
    if image_name:
        image = await Image.query.where(Image.name == image_name).gino.first()
    elif image_id:
        image = await Image.get(image_id)
    else:
        image = None
        # если не указана картинка смотрим, что там в логе
        if log and log.name:
            image = await Image.query.where(Image.name == log.name).gino.first()

    # в любом случае удаляем комманду пользователя, так как  она не нужна
    await _delete_mess(bot, message.chat.id, message.message_id)

    if log and image:
        # если сообщение есть, то нужно его апдейтить
        try:
            await bot(
                EditMessageMedia(
                    chat_id=log.chat_id,
                    message_id=log.message_id,
                    # надо достать айдишник картинки с серверов телеги
                    media=InputMediaPhoto(media=image.file_id, caption=MESS),
                    reply_markup=keyboard,
                )
            )
            await log.update(name=image.name).apply()
        except TelegramBadRequest as e:
            print(f"!!!! {str(e)}")
            # если не удалось апдейтить, то удалем и шлём новое
            await _delete_mess(bot, log.chat_id, log.message_id)
            await _send_new_mess(message, MESS, keyboard, mode, image)
    else:
        await _send_new_mess(message, MESS, keyboard, mode, None)


async def _delete_mess(bot, chat_id: int, mess_id: int):
    """обрабатываю исключения"""
    try:
        await bot(DeleteMessage(chat_id=chat_id, message_id=mess_id))
    except TelegramBadRequest:
        pass
    except TelegramNotFound:
        pass


async def _send_new_mess(message, MESS, keyboard, mode, image):
    # если нет логов, то нужно отправить новое сообщение и записать его в логи
    if image:
        message = await message.answer_photo(
            # BufferedInputFile(image.file, filename=image.name + ".png"),
            photo=image.file_id,
            caption=MESS,
            parse_mode=mode,
            reply_markup=keyboard,
        )
        await ImageLog.delete.where(ImageLog.chat_id == message.chat.id).gino.status()
        await ImageLog.create(
            chat_id=message.chat.id, message_id=message.message_id, name=image.name
        )
        return message
    else:
        # вариант без картинки
        message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)
        await ImageLog.delete.where(ImageLog.chat_id == message.chat.id).gino.status()
        await ImageLog.create(chat_id=message.chat.id, message_id=message.message_id)
