from aiogram.filters.callback_data import CallbackData


class CallProfession(CallbackData, prefix="t"):
    action: str
    profession: str
