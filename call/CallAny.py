from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CallAny(CallbackData, prefix="any"):
    action: str
    user_id: int = 0
    person_id: int = 0
    gametime: int = 0
    inventory_id: int = 0
    item_id: int = 0
    equip: bool = False
    action_id: int = 0
    event_id: int = 0
    avatar: Optional[int] = None
