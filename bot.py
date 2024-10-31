import logging
from zoneinfo import ZoneInfo
from aiogram import Dispatcher, Bot, F
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder
from aiogram.filters.command import CommandStart

from config import BOT_TOKEN, REDIS_URL
import asyncio
from logging_config import setup_logging
from logging_middleware import LoggingMiddleware
from database.db import DataBaseSession
from database.engine import session_maker, create_db, drop_db
from handlers import setup_routers
from handlers.subscribe import handle_subscribe

from users_middleware import UsersMiddleware


from keyboards.choise_subcath import setup_dialogs, sub_cathegories

bot = Bot(BOT_TOKEN)

storage = RedisStorage.from_url(REDIS_URL, key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True)
)



            

        

async def main():
    setup_logging()
    dp = Dispatcher(storage = storage)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    # await drop_db()
    await create_db()
    router = setup_routers()
    # dp.include_router(dialog)
    dp.include_router(router)
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(UsersMiddleware())
    dp.callback_query.register(handle_subscribe, F.data.startswith('subcath'))
    # dp.message.register(handle_subscribe, F.text == '/subscribe')
    print('Бот запущен и готов к приему сообщений')
    logging.info('--------------------Бот запущен и готов к приему сообщений------------------------------')

    await bot.delete_webhook(drop_pending_updates=True)
    setup_dialogs(dp)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True)
    

if __name__ == "__main__":
    asyncio.run(main())

