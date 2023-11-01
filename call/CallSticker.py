from aiogram.filters.callback_data import CallbackData


class CallSticker(CallbackData, prefix="t"):
    action: str
    sticker_id: int
