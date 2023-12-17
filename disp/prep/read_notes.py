from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F


from func import update_message, add_keyboard, person_note_read
from mdls import PersonNote, NoteText
from call import CallPerson, CallNotes


@router.callback_query(CallNotes.filter(F.action == "read_notes"))
async def read_notes(callback: CallbackQuery, callback_data: CallNotes):
    """
    кароч тут вытаскиваются все записи разом в отсортированном виде
    а потом выбираем запись по геймтайму, который тут не геймтайм,
    а номер записи в списке
    последний с конца -1
    предпоследний -2
    предпредпоследний -3
    если берем 0 - пишем что таких записей еще не было
    """
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
                    action="prep_main",
                    person_id=callback_data.person_id,
                    profession=callback_data.profession,
                    i_id=callback_data.i_id,
                ).pack(),
                "  >>": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    profession=callback_data.profession,
                    i_id=callback_data.i_id,
                    gametime=callback_data.gametime + 1,
                ).pack(),
            }

        else:
            mess = person_note_read(note)
            DICT = {
                "<<  ": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    profession=callback_data.profession,
                    i_id=callback_data.i_id,
                    gametime=callback_data.gametime - 1,
                ).pack(),
                "назад": CallPerson(
                    action="prep_main",
                    person_id=callback_data.person_id,
                    profession=callback_data.profession,
                    i_id=callback_data.i_id,
                ).pack(),
                "  >>": CallNotes(
                    action="read_notes",
                    person_id=callback_data.person_id,
                    profession=callback_data.profession,
                    i_id=callback_data.i_id,
                    gametime=callback_data.gametime + 1,
                ).pack(),
            }
    else:
        mess = "Более свежих записей нет"
        DICT = {
            "<<  ": CallNotes(
                action="read_notes",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                i_id=callback_data.i_id,
                gametime=callback_data.gametime - 1,
            ).pack(),
            "назад": CallPerson(
                action="prep_main",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                i_id=callback_data.i_id,
            ).pack(),
        }
    await update_message(callback.message, mess, add_keyboard(DICT, True), True)
