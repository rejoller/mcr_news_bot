from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database.models import Subscriptions
from datetime import datetime as dt
from icecream import ic
import logging




router = Router()


@router.callback_query(F.data.startswith('subscribe_'))
async def handle_get_subscribe(query: types.CallbackQuery, session: AsyncSession, bot: Bot):
    cathegory_id = int(query.data.split('_')[1])
    cathegory_name = query.data.split('_')[2]
    ic(cathegory_id, cathegory_name)
    user_id = query.from_user.id
    sql_query = insert(Subscriptions).values(
        user_id=user_id,
        cathegory_id=cathegory_id
    )
    try:
        await session.execute(sql_query)    
        await session.commit()
        await session.close()
    
        await query.message.answer(f'Вы подписались на категорию {cathegory_name}')
        await query.answer()
        
    except IntegrityError as e:
        logging.error(e)
        await query.message.answer(f'Вы уже подписаны на категорию {cathegory_name}')
        await query.answer()