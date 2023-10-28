from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_keyboard(DICT: dict) -> "InlineKeyboardMarkup":
    "Создаем клавиатуру на основе словаря кнопок с калбеками"

    keyboard = []
    for key, value in DICT.items():
        keyboard.append(InlineKeyboardButton(text=key, callback_data=value))

    kb = InlineKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, inline_keyboard=[keyboard]
    )
    return kb
