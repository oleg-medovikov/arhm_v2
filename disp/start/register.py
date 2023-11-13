from disp.start import router
import asyncio
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Bot
from random import randint

from func import update_message, add_keyboard, update_sticker, person_create
from mdls import MessText, PersonName
from call import CallUser, CallSex, CallProfession, CallGamename, CallPerson


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
    # кидаем кубик на статы и вытаскиваем на время ктулху
    value = randint(1,6)
    await state.update_data(dice=value)
    await update_sticker(callback.from_user.id, 'ктулху', bot)
    mess = await MessText.get('cthulhu_dice')
    if mess is not None:
        mess = mess.text + f'\n{value}\ufe0f\u20e3'
    else:
        mess = f'\n{value}\ufe0f\u20e3'
    message = await update_message(callback.message, mess, None)
    # даем пользователю прочитать и меняем сообщение
    # тут же создаем нового персонажа
    user_data = await state.get_data()
    person = await person_create(user_data)
    await asyncio.sleep(5)

    mess_name = {
            1: f'register_dice_{user_data["profession"]}_1-2',    
            2: f'register_dice_{user_data["profession"]}_1-2',    
            3: f'register_dice_{user_data["profession"]}_3-4',    
            4: f'register_dice_{user_data["profession"]}_3-4',    
            5: f'register_dice_{user_data["profession"]}_5-6',    
            6: f'register_dice_{user_data["profession"]}_5-6',    
            }[value]
    DICT = {
        'уйти из полицейского участка': CallPerson(action='continue_game', person_id=person.id).pack()
            }

    await update_sticker(callback.from_user.id, 'шериф', bot)
    mess = await MessText.get(mess_name)
    return await update_message(message, mess.text, add_keyboard(DICT))
