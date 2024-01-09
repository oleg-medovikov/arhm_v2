from disp.prep import router
from aiogram.types import CallbackQuery
from aiogram import F, Bot

from func import update_message, add_keyboard
from mdls import User, UserImage, MessText
from call import CallAny


@router.callback_query(CallAny.filter(F.action == "avatar_main"))
async def avatar_main(callback: CallbackQuery, callback_data: CallAny, bot: Bot):
    """
    тут надо узнать, есть ли у юзера загруженные картинки,
    выдать ему список загруженных аватарок
    предложить загрузить новую картинку
    или вернуться к стандартной картинке
    """
    if callback_data.user_id:
        images = await UserImage.query.where(
            UserImage.user == callback_data.user_id
        ).gino.all()
    else:
        images = (
            await UserImage.query.where(User.tg_id == callback.message.chat.id)
            .join(User)
            .gino.all()
        )

    DICT = {}
    avatar = callback_data.avatar
    if not images:
        mess = await MessText.get("avatar_main_no_foto")
    else:
        mess = await MessText.get("avatar_main_foto")
        callback_data.action = "avatar_change"
        for image in images:
            callback_data.avatar = image.id
            DICT[image.name] = callback_data.pack()

        callback_data.avatar = -1
        DICT["стандартная"] = callback_data.pack()

    callback_data.avatar = avatar
    callback_data.action = "avatar_upload"
    DICT["новая фотокарточка"] = callback_data.pack()

    callback_data.action = "prep_main"
    DICT["назад"] = callback_data.pack()

    await update_message(
        bot,
        callback.message,
        mess,
        add_keyboard(DICT, True),
        True,
        image_user=callback_data.avatar,
        image_name=callback_data.profession,
    )
