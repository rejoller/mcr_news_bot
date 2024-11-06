from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from database.models import Subscriptions, Subcategories

router = Router()


@router.message(Command('my_subscriptions'), F.chat.type == "private")
async def handle_start(message: Message, session: AsyncSession):
    
    query = select(
        Subscriptions.category_id, Subcategories.subcategory_name).where(
        Subscriptions.user_id == message.from_user.id
    ).join(Subcategories, Subscriptions.category_id == Subcategories.subcategory_id)
        
    response = await session.execute(query)
    result = response.all()
    if not result:
        await message.answer("Вы не подписаны ни на одну категорию, для того чтобы подписаться нажмите на команду /subscribe")
        return
    
    cathegories_id = [i for i in result]
    
    builder = InlineKeyboardBuilder()
    for id, name in cathegories_id:
        builder.button(text=name, callback_data=f'msgcat:{id}')
    builder.adjust(1)
    
    await message.answer("Ваши подписки", reply_markup=builder.as_markup())
    
