from datetime import datetime, timedelta
from mdls import PersonNote


def person_note_read(note: "PersonNote") -> str:
    DAYS = note.gametime // 96
    TIME = (
        datetime.strptime("09:00", "%H:%M") + timedelta(minutes=15 * note.gametime)
    ).strftime("%H:%M")

    LIST = (
        f"\n<b>Проведено дней в Археме:</b> {DAYS}",
        f"\n<b>Время записи:</b> {TIME}",
        "\n\n",
        "<blockquote>",
        note.note_text.text,
        "</blockquote>",
    )

    MESS = "".join(str(x) for x in LIST)
    return MESS
