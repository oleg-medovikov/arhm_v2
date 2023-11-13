from sqlalchemy import and_

from mdls import Person, PersonNote, NoteText


async def add_person_note(person: "Person", text: str):
    # нужно посмотреть есть ли NoteText с таким text

    note_text = await NoteText.query.where(NoteText.text == text).gino.first()
    if note_text is None:
        note_text = await NoteText.create(text=text)

    # создаем запись в дневнике

    person_note = await PersonNote.query.where(
        and_(PersonNote.p_id == person.id, PersonNote.gametime == person.gametime)
    ).gino.first()
    if person_note is None:
        await PersonNote.create(
            p_id=person.id, gametime=person.gametime, n_id=note_text.id
        )
