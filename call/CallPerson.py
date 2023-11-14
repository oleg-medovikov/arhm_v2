from aiogram.filters.callback_data import CallbackData


class CallPerson(CallbackData, prefix="t"):
    action: str
    person_id: int
    profession: str
    i_id: int
