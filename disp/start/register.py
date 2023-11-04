from disp.start import router
import asyncio
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Bot
from aiogram.enums.dice_emoji import DiceEmoji

from func import update_message, add_keyboard, update_sticker
from func.system.delete_message import delete_message
from mdls import MessText, PersonName
from call import CallUser, CallSex, CallProfession, CallGamename


class NewPerson(StatesGroup):
    user_id = State()
    gamename = State()
    sex = State()
    profession = State()
    dice = State()


@router.callback_query(CallUser.filter(F.action == "register"))
async def register_1_ask_sex(callback: CallbackQuery, callback_data: CallUser, state: FSMContext):
    user_id = callback_data.user_id
    await state.update_data(user_id=user_id)
    mess = await MessText.get("register_sex")

    DICT = {
        "Мужчина": CallSex(action="ask_sex", sex=True).pack(),
        "Женщина": CallSex(action="ask_sex", sex=False).pack(),
    }
    return await update_message(callback.message, mess.text, add_keyboard(DICT))


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


@router.callback_query(CallProfession.filter(F.action == "ask_profession"))
async def register_3_ask_gamename(
        callback: CallbackQuery, callback_data: CallProfession, state: FSMContext, bot: Bot
):
    profession = callback_data.profession
    await state.update_data(profession=profession)

    mess = await MessText.get(f"register_name_{profession}")
    names = await PersonName.query.where(PersonName.profession == profession).gino.all()
    DICT = {}
    for name in names: 
        DICT[name.gamename] = CallGamename(action='ask_gamename', gamename=name.gamename).pack()

    await update_sticker(callback.from_user.id, 'шериф', bot)
    return await update_message(callback.message, mess.text, add_keyboard(DICT))


@router.callback_query(CallGamename.filter(F.action == "ask_gamename"))
async def register_4_ask_destination(callback: CallbackQuery, callback_data: CallGamename, state: FSMContext):
    gamename = callback_data.gamename
    await state.update_data(gamename=gamename)
    user_data = await state.get_data()
    mess = await MessText.get(f"register_ask_destination_{user_data['profession']}")
    destination = await MessText.get(f"register_destination_{user_data['profession']}")
    DICT = {
            destination.text: 'register_destination'
            }
    return await update_message(callback.message, mess.text, add_keyboard(DICT))


@router.callback_query(F.data == "register_destination")
async def register_5_ask_dice(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    mess = await MessText.get(f"register_dice_{user_data['profession']}")
    DICT = {"Отдать письмо": "register_dice"}
    return await update_message(callback.message, mess.text, add_keyboard(DICT))


@router.callback_query(F.data == "register_dice")
async def register_6_end(callback: CallbackQuery, state: FSMContext, bot:Bot):
    if callback.message is not None:
        await delete_message(callback.message)

    msg = await bot.send_dice(callback.from_user.id, emoji=DiceEmoji.DICE)
    if msg.dice is not None:
        value = msg.dice.value
    else:
        value = 1
    await state.update_data(dice=value)
    await asyncio.sleep(4)
    # await bot.delete_message(msg.chat.id, msg.message_id)
    user_data = await state.get_data()

    mess_name = {
            1: f'register_dice_{user_data["profession"]}_1-2',    
            2: f'register_dice_{user_data["profession"]}_1-2',    
            3: f'register_dice_{user_data["profession"]}_3-4',    
            4: f'register_dice_{user_data["profession"]}_3-4',    
            5: f'register_dice_{user_data["profession"]}_5-6',    
            6: f'register_dice_{user_data["profession"]}_5-6',    
            }[value]

    mess = await MessText.get(mess_name)
    await update_message(callback.message, mess.text, None)
