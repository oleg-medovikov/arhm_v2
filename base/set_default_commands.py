from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: "Bot") -> None:
    "Создаем кнопки для меню бота"
    DICT = {
        "/start": "Приветсвие",
    }
    LIST = []

    for key, value in DICT.items():
        LIST.append(BotCommand(command=key, description=value))

    await bot.set_my_commands(LIST)
