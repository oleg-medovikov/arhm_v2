from aiogram.types import Message
from aiogram.filters import Command
from pandas import DataFrame
from aiogram.types.input_file import BufferedInputFile


from disp import dp
from func import delete_message, write_styling_excel
from mdls import User, MessText


COMMANDS = [
    "MessText",
]


@dp.message(Command(commands=COMMANDS))
async def get_files(message: Message):
    await delete_message(message)

    user = await User.query.where(User.tg_id == message.chat.id).gino.first()
    if user is None or not user.admin:
        return None

    COMMAND = str(message.text).replace("/", "")

    LIST = {
        "MessText": MessText.query.gino.all(),
    }.get(COMMAND)

    COLUMNS = {
        "MessText": ["name", "text", "date_update"],
    }.get(COMMAND)

    if LIST is None:
        return None

    LIST = await LIST

    df = DataFrame(data=[_.to_dict() for _ in LIST])
    df = df[COLUMNS]

    FILEPATH = f"/tmp/{COMMAND}.xlsx"
    FILENAME = FILEPATH.rsplit("/", 1)[-1]
    SHETNAME = "def"
    write_styling_excel(FILEPATH, df, SHETNAME)

    file = BufferedInputFile(open(FILEPATH, "rb").read(), FILENAME)
    return await message.answer_document(file)
