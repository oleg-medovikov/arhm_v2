import asyncio

from disp import dp, bot
from base import db
from func import set_default_commands
from conf import settings


async def on_startup():
    await db.set_bind(settings.PSQL)
    await db.gino.create_all()
    await set_default_commands(bot)
    await dp.start_polling(bot)


async def on_shutdown():
    await db.pop_bind().close()


if __name__ == "__main__":
    try:
        asyncio.run(on_startup())
    except KeyboardInterrupt:
        asyncio.run(on_shutdown())
