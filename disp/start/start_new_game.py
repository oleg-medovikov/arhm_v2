from aiogram.types import CallbackQuery
from aiogram import F

from disp import dp
from func import add_keyboard, update_message


@dp.callback_query(F.data == "start_new_game")
async def start_new_game(callback: CallbackQuery):
    """
    Если есть живой персонаж, говорим, что уже видели игрока, предлагаем
    продолжить игру или прочесть правила.
    Если нет живого персонажа, встречаем запугиванием и заставляем пройти анкету.

    """

    DICT = {
        "продолжим игру": "continue_game",
    }

    await update_message(callback.message, "нашел персонажа", add_keyboard(DICT))
