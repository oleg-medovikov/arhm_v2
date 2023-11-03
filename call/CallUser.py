from aiogram.filters.callback_data import CallbackData


class CallUser(CallbackData, prefix="t"):
    action: str
    user_id: int
