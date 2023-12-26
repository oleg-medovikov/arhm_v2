from typing import Optional
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from mdls import Sticker, StickerLog


async def update_sticker(chat_id: int, sticker_name: Optional[str], bot: Bot):
    log = await StickerLog.get(chat_id)
    if log is not None:
        if log.name == sticker_name and sticker_name != "ктулху":
            # если стикер в замене не нуждается, то выходим
            return
        # иначе удалем текущий стикер
        try:
            await bot.delete_message(chat_id, log.message_id)
        except TelegramBadRequest:
            pass

    if sticker_name is not None:
        sticker = await Sticker.query.where(Sticker.name == sticker_name).gino.first()
        if sticker is not None:
            try:
                MESS = await bot.send_sticker(
                    chat_id, sticker=sticker.send_id, protect_content=True
                )
            except TelegramBadRequest:
                pass
            else:
                if log is not None:
                    await log.update(message_id=MESS.message_id).apply()
                else:
                    await StickerLog.create(
                        chat_id=chat_id, message_id=MESS.message_id, name=sticker_name
                    )
