from aiogram import Bot, Router, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


BOT_TOKEN  = '6569068360:AAEUN1C31L78AAFwuztKdrM4q5xyeHBSuyk'
bot = Bot(token=BOT_TOKEN)

router = Router()

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)



