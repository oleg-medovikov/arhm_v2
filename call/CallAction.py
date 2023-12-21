from aiogram.filters.callback_data import CallbackData


class CallAction(CallbackData, prefix="t"):
    action: str
    person_id: int
    profession: str
    loc_id: int
    action_id: int
    event: int
