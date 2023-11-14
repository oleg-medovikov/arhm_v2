from aiogram.filters.callback_data import CallbackData


class CallInventory(CallbackData, prefix="t"):
    action: str
    person_id: int
    profession: str
    i_id: int
    item: int
