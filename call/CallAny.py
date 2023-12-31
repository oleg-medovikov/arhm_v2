from aiogram.filters.callback_data import CallbackData
from ast import literal_eval


class CallAny(CallbackData, prefix="t"):
    action: str
    person: str
    meta: str

    def unpack_person(self):
        list_ = self.person.split(",")
        d = {
            "id": int(list_[0]),
            "loc_id": int(list_[1]),
            "i_id": int(list_[2]),
            "profession": list_[3],
            "avatar": None if list_[4] == "" else list_[4],
        }
        return d

    def unpack_meta(self):
        return literal_eval(self.meta.replace("%3A", ":"))

    @staticmethod
    def pack_meta(d: dict):
        return str(d).replace(" ", "").replace(":", "%3A")
