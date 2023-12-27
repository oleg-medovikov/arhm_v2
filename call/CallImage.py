from aiogram.filters.callback_data import CallbackData


class CallImage(CallbackData, prefix="t"):
    action: str
    image_id: int
