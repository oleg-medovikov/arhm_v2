from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, person_note_read
from mdls import PersonNote, NoteText
from call import CallPerson, CallNotes


@router.callback_query(CallNotes.filter(F.action == "read_notes"))
async def read_notes(callback: CallbackQuery, callback_data: CallNotes, bot: Bot):
    if callback_data.gametime != 0:
        notes = (
            await PersonNote.load(note_text=NoteText)
            .query.where(PersonNote.p_id == callback_data.person_id)
            .order_by(PersonNote.gametime)
            .gino.all()
        )
        try:
            note = notes[callback_data.gametime]
        except IndexError:
            mess = (
                "Тут старые записи, не имеющие отношения к вашим приключениям в городе"
            )
            DICT = {
                "назад": CallPerson(
                    action="prep_main", person_id=callback_data.person_id
                ).pack(),
                "  >>": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    gametime=callback_data.gametime + 1,
                ).pack(),
            }

        else:
            mess = person_note_read(note)
            DICT = {
                "<<  ": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    gametime=callback_data.gametime - 1,
                ).pack(),
                "назад": CallPerson(
                    action="prep_main", person_id=callback_data.person_id
                ).pack(),
                "  >>": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    gametime=callback_data.gametime + 1,
                ).pack(),
            }
    else:
        mess = "Более свежих записей нет"
        DICT = {
            "<<  ": CallNotes(
                action="read_notes",
                person_id=callback_data.person_id,
                gametime=callback_data.gametime - 1,
            ).pack(),
            "назад": CallPerson(
                action="prep_main", person_id=callback_data.person_id
            ).pack(),
        }

    await update_message(callback.message, mess, add_keyboard(DICT, True), True)
