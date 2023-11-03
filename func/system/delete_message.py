from aiogram.exceptions import TelegramNotFound, TelegramBadRequest
from aiogram.types import Message


async def delete_message(message: Message) -> None:
    "удаление сообщения с обработкой исключения"

    try:
        await message.delete()
    except TelegramNotFound:
        pass
    except TelegramBadRequest:
        pass
