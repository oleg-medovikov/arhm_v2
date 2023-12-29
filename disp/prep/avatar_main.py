from disp.prep import router
from aiogram.types import CallbackQuery, message
from aiogram import F, Bot

from func import update_message, add_keyboard
from mdls import User, Person, UserImage, MessText
from call import CallPerson, CallAvatar


@router.callback_query(CallPerson.filter(F.action == "avatar_main"))
async def avatar_main(callback: CallbackQuery, callback_data: CallPerson, bot: Bot):
    """
    тут надо узнать, есть ли у юзера загруженные картинки,
    выдать ему список загруженных аватарок
    предложить загрузить новую картинку
    или вернуться к стандартной картинке
    """
    images = (
        UserImage.query.where(User.tg_id == callback.message.chat.id)
        .join(User)
        .gino.all()
    )

    DICT = {}
    if not images:
        mess = await MessText.get("avatar_main_no_foto")
    else:
        mess = await MessText.get("avatar_main_foto")
        for image in images:
            DICT[image.name] = CallAvatar(
                action="avatar_change",
                person_id=callback_data.person_id,
                profession=callback_data.profession,
                i_id=callback_data.i_id,
                image_guid=str(image.guid),
            ).pack()

        DICT["стандартная"] = CallAvatar(
            action="avatar_change",
            person_id=callback_data.person_id,
            profession=callback_data.profession,
            i_id=callback_data.i_id,
            image_guid="standart",
        ).pack()

    DICT["новая фотокарточка"] = CallPerson(
        action="avatar_upload",
        person_id=callback_data.person_id,
        profession=callback_data.profession,
        i_id=callback_data.i_id,
    ).pack()

    DICT["назад"] = CallPerson(
        action="prep_main",
        person_id=callback_data.person_id,
        profession=callback_data.profession,
        i_id=callback_data.i_id,
    ).pack()

    await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT, True),
        True,
        image_user=callback_data.avatar,
        image_name=callback_data.profession,
    )
