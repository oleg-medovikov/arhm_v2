from disp.start import router
import asyncio
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Bot
from aiogram.enums.dice_emoji import DiceEmoji

from func import update_message, add_keyboard
from mdls import MessText, Sticker, PersonName
from call import CallSex, CallProfession, CallGamename


class NewPerson(StatesGroup):
    msg = State()
    gamename = State()
    sex = State()
    profession = State()
    destination = State()
    dise = State()


@router.callback_query(F.data == "register")
async def register_1_ask_sex(callback: CallbackQuery, state: FSMContext):
    mess = await MessText.get("register_sex")

    DICT = {
        "Мужчина": CallSex(action="ask_sex", sex=True).pack(),
        "Женщина": CallSex(action="ask_sex", sex=False).pack(),
    }
    await update_message(callback.message, mess.text, add_keyboard(DICT))
    # Устанавливаем пользователю состояние "пишет название"
    # await state.set_state(NewPerson.sex)


@router.callback_query(CallSex.filter(F.action == "ask_sex"))
async def register_2_ask_profession(
    callback: CallbackQuery, callback_data: CallSex, state: FSMContext
):
    sex = callback_data.sex

    if sex:
        mess = await MessText.get("register_no_men")
        DICT = {
            "Мужчина": CallSex(action="ask_sex", sex=True).pack(),
            "Женщина": CallSex(action="ask_sex", sex=False).pack(),
        }
        return await update_message(callback.message, mess.text, add_keyboard(DICT))

    await state.update_data(sex=sex)
    mess = await MessText.get("register_profession")
    if sex:
        DICT = {}
    else:
        DICT = {
            "студентка": CallProfession(
                action="ask_profession", profession="студентка"
            ).pack(),
        }
    return await update_message(callback.message, mess.text, add_keyboard(DICT))
    # await state.set_state(NewPerson.profession)


@router.callback_query(CallProfession.filter(F.action == "ask_profession"))
async def register_3_ask_gamename(
    callback: CallbackQuery, callback_data: CallProfession, state: FSMContext
):
    profession = callback_data.profession
    await state.update_data(profession=profession)

    mess = await MessText.get(f"register_name_{profession}")
    names = await PersonName.query.where(PersonName.profession == profession).gino.all()
    DICT = {}
    for name in names: 
        DICT[name.gamename] = CallGamename(action='ask_gamename', gamename=name.gamename).pack()

    return await update_message(callback.message, mess.text, add_keyboard(DICT))


@router.callback_query(CallGamename.filter(F.action == "ask_gamename"))
async def register_4_ask_destination(callback: CallbackQuery, callback_data: CallGamename, state: FSMContext):
    gamename = callback_data.gamename
    await state.update_data(gamename=gamename)
    mess = await MessText.get("register_ask_destination")
    user_data = await state.get_data()
    destination = await MessText.get(f"register_destination_{user_data['profession']}")
    DICT = {
            destination.text: 'register_destination'
            }
    await update_message(callback.message, mess.text, add_keyboard(DICT))
    #await state.set_state(NewPerson.destination)


@router.callback_query(F.data == "register_destination")
async def register_5_ask_dise(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    mess = await MessText.get(f"register_dise_{user_data['profession']}")
    DICT = {"Отдать письмо": "register_dice"}
    await update_message(callback.message, mess.text, add_keyboard(DICT))


@router.callback_query(F.data == "register_dice")
async def register_6_end(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    msg = await bot.send_dice(callback_query.message.chat.id, emoji=DiceEmoji.DICE)
    await state.update_data(dice=msg.dice.value)
    await asyncio.sleep(3)
    mess = f"Вам выпало {msg.dice.value}"
    await update_message(callback_query.message, mess, None)
