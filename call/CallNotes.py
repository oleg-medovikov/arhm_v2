from aiogram.filters.callback_data import CallbackData


class CallNotes(CallbackData, prefix="t"):
    action: str
    person_id: int
    profession: str
    i_id: int
    gametime: int
