from disp.excel import router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import F, Bot

from call import CallImage
from mdls import Image


class NewImage(StatesGroup):
    image_id = State()
    name = State()
    category = State()


@router.callback_query(CallImage.filter(F.action == "ask_name_Image"))
async def ask_Image_name(
    callback: CallbackQuery, callback_data: CallImage, state: FSMContext
):
    await state.update_data(image_id=callback_data.image_id)

    await callback.message.answer("Напишите название картинки:")
    # Устанавливаем пользователю состояние "пишет название"
    return await state.set_state(NewImage.name)


@router.message(NewImage.name)
async def ask_Image_category(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="Теперь напишите категорию",
    )
    return await state.set_state(NewImage.category)


@router.message(NewImage.category)
async def update_Image(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    user_data = await state.get_data()
    image = await Image.get(user_data["image_id"])

    await image.update(name=user_data["name"], category=user_data["category"]).apply()

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()

    # await bot.send_sticker(message.chat.id, image.file)
    return await message.answer(f'Картинка сохранена\nid: {user_data["image_id"]}')
