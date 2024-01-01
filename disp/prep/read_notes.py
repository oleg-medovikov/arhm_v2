from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot


from func import update_message, add_keyboard, person_note_read
from mdls import PersonNote, NoteText
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "read_notes"))
async def read_notes(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут вытаскиваются все записи разом в отсортированном виде
    а потом выбираем запись по геймтайму, который тут не геймтайм,
    а номер записи в списке
    последний с конца -1
    предпоследний -2
    предпредпоследний -3
    если берем 0 - пишем что таких записей еще не было
    """
    # кнопка назад
    callback_data.action = "prep_main"
    call_back = callback_data.pack()
    # кнопка вперед
    callback_data.action = "read_notes"
    callback_data.gametime += 1
    call_next = callback_data.pack()
    # кнопка назад
    callback_data.action = "read_notes"
    callback_data.gametime -= 2
    call_prev = callback_data.pack()
    # возвразаем значение назад
    callback_data.gametime += 1

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
                "назад": call_back,
                "  >>": call_next,
            }
        else:
            mess = person_note_read(note)
            DICT = {
                "<<  ": call_prev,
                "назад": call_back,
                "  >>": call_next,
            }
    else:
        mess = "Более свежих записей нет"
        DICT = {
            "<<  ": call_prev,
            "назад": call_back,
        }
    await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT, True),
        True,
        image_name="дневник",
    )
