
import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Main_cathegories
from icecream import ic

router = Router()

@router.message(Command('subscribe'), F.chat.type == 'private')
async def manual_check_news(message: Message, session: AsyncSession, bot: Bot):
    
    builder = InlineKeyboardBuilder()
    
    check_query = select(Main_cathegories.main_cathegory_id, Main_cathegories.main_cathegory_name)
    result = await session.execute(check_query)
    response = result.all()
    
    
    for index, value in enumerate(response, start=1):
        ic(value[0], value[1])
        builder.button(text=str(value[1]), callback_data=f'subcath:{value[1]}:{value[0]}')
    builder.adjust(1)
    
    await message.answer('Выберите категорию', reply_markup=builder.as_markup())
    
    