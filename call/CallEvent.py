from aiogram.filters.callback_data import CallbackData


class CallEvent(CallbackData, prefix="t"):
    action: str
    person_id: int
    profession: str
    i_id: int
    event: int
    choice: int
    event_time: int
