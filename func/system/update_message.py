from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNotFound
from typing import Optional
from aiogram.types import Message, InlineKeyboardMarkup


async def update_message(
    message: Optional[Message],
    MESS,
    keyboard: Optional[InlineKeyboardMarkup],
    html: bool = False,
) -> Optional["Message"]:
    "изменение сообщения с обработкой исключений"
    if message is None:
        return
    if html:
        mode = "html"
    else:
        mode = "Markdown"

    try:
        await message.delete()
    except TelegramBadRequest:
        message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)
    except TelegramNotFound:
        message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)
    else:
        message = await message.answer(MESS, reply_markup=keyboard, parse_mode=mode)

    return message
