from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_keyboard(DICT: dict, line: bool = False) -> "InlineKeyboardMarkup":
    "Создаем клавиатуру на основе словаря кнопок с калбеками"
    if line:
        keyboard = []
        list_ = []
        for key, value in DICT.items():
            list_.append(InlineKeyboardButton(text=key, callback_data=value))

        keyboard.append(list_)
    else:
        keyboard = []
        for key, value in DICT.items():
            list_ = []
            list_.append(InlineKeyboardButton(text=key, callback_data=value))
            keyboard.append(list_)

    kb = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        inline_keyboard=keyboard,
    )
    return kb
