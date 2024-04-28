from aiogram import Bot, Router, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


BOT_TOKEN  = ''
bot = Bot(token=BOT_TOKEN)

router = Router()

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)



