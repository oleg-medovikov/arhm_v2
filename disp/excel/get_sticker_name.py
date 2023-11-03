from disp.excel import router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F

from call import CallSticker
from mdls import Sticker


class NewSticker(StatesGroup):
    sticker_id = State()
    name = State()
    category = State()


@router.callback_query(CallSticker.filter(F.action == "ask_name"))
async def ask_sticker_name(
    callback: CallbackQuery, callback_data: CallSticker, state: FSMContext
):
    await state.update_data(sticker_id=callback_data.sticker_id)

    await callback.message.answer("Напишите название стикера:")
    # Устанавливаем пользователю состояние "пишет название"
    await state.set_state(NewSticker.name)


@router.message(NewSticker.name)
async def ask_sticker_category(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="Теперь напишите категорию",
    )
    await state.set_state(NewSticker.category)


@router.message(NewSticker.category)
async def update_sticker(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    user_data = await state.get_data()

    await Sticker.update.values(
        name=user_data["name"], category=user_data["category"]
    ).where(Sticker.id == user_data["sticker_id"]).gino.status()

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()
    return await message.answer(f'Стикер сохранен\nid: {user_data["sticker_id"]}')
