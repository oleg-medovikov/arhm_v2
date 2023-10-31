from disp.excel import router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.input_file import BufferedInputFile

from func import (
    delete_message,
    write_styling_excel,
    get_all_MessText,
    get_all_Location,
    get_all_PersonDefault,
    get_all_Sticker,
    get_all_Item,
)
from mdls import User


COMMANDS = ["MessText", "Location", "PersonDefault", "Sticker", "Item"]


@router.message(Command(commands=COMMANDS))
async def get_files(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    COMMAND = str(message.text).replace("/", "")

    FUNC = {
        "MessText": get_all_MessText(),
        "Location": get_all_Location(),
        "PersonDefault": get_all_PersonDefault(),
        "Sticker": get_all_Sticker(),
        "Item": get_all_Item(),
    }.get(COMMAND)

    if FUNC is None:
        return None

    df = await FUNC

    FILEPATH = f"/tmp/{COMMAND}.xlsx"
    FILENAME = FILEPATH.rsplit("/", 1)[-1]
    SHETNAME = "def"
    write_styling_excel(FILEPATH, df, SHETNAME)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
