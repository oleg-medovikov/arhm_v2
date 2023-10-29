from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from typing import Optional
from aiogram.types import Message, InlineKeyboardMarkup


async def update_message(
    message: Optional[Message], MESS, keyboard: InlineKeyboardMarkup
) -> None:
    "изменение сообщения с обработкой исключений"
    if message is None:
        return

    try:
        await message.edit_text(MESS, parse_mode="Markdown")
    except TelegramBadRequest:
        await message.delete()
        await message.answer(MESS, reply_markup=keyboard, parse_mode="Markdown")
    except TelegramNotFound:
        await message.answer(MESS, reply_markup=keyboard, parse_mode="Markdown")

    try:
        await message.edit_reply_markup(reply_markup=keyboard)
    except TelegramNotFound:
        pass
