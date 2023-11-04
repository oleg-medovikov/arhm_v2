from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from typing import Optional
from aiogram.types import Message, InlineKeyboardMarkup


async def update_message(
    message: Optional[Message], MESS, keyboard: Optional[InlineKeyboardMarkup]
) -> Optional["Message"]:
    "изменение сообщения с обработкой исключений"
    if message is None:
        return

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    try:
        await message.edit_text(MESS, parse_mode="Markdown")
    except TelegramBadRequest:
        try:
            await message.delete()
        except TelegramBadRequest:
            pass
        await message.answer(MESS, reply_markup=keyboard, parse_mode="Markdown")
    except TelegramNotFound:
        await message.answer(MESS, reply_markup=keyboard, parse_mode="Markdown")

    if keyboard is not None:
        try:
            await message.edit_reply_markup(reply_markup=keyboard)
        except TelegramNotFound:
            pass
        except TelegramBadRequest:
            pass

    return message
