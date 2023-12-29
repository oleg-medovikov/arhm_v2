from aiogram.filters.callback_data import CallbackData


class CallAny(CallbackData, prefix="t"):
    action: str
    person: str
    meta: str
