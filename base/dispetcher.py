import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from conf import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("schedule").propagate = False
logging.getLogger("schedule").addHandler(logging.NullHandler())
logging.getLogger("gino.engine._SAEngine").setLevel(logging.ERROR)

bot = Bot(token=settings.BOT_API)
dp = Dispatcher(storage=MemoryStorage())
