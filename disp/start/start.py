from aiogram.types import Message
from aiogram.filters import CommandStart

from disp import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    return await message.answer("Привет!")
