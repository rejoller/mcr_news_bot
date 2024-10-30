import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database.models import News_cathegories, Subscriptions




router=Router()




@router.message(Command('my_subscriptions'), F.chat.type == 'private')
async def show_my_subscriptions(message: Message, session: AsyncSession):
    
    user_id = message.from_user.id

    query = select(News_cathegories.cathegory_name) \
                    .join(Subscriptions, and_(Subscriptions.cathegory_id == News_cathegories.cathegory_id,
                    Subscriptions.user_id == user_id))
                    
    result = await session.execute(query)
    response = result.all()
    
    try:
        await message.answer(f'<b>Ваши подписки:</b>\n{"\n".join(item[0] for item in response)}', parse_mode='HTML')
    except Exception as e:
        logging.error(e)