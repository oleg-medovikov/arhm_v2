from aiogram.filters.callback_data import CallbackData


class CallSex(CallbackData, prefix="t"):
    action: str
    sex: int
