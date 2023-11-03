from aiogram.filters.callback_data import CallbackData


class CallGamename(CallbackData, prefix="t"):
    action: str
    gamename: str
