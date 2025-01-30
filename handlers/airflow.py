from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession


from filters.admins import AdminFilter

router = Router()



@router.message(Command('airflow'), F.chat.type == "private")
async def handle_start(message: Message, session: AsyncSession):
    

    
    text = 'посмотреть информацию о DAG'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, callback_data='dag_info')
        ]
    ])
    
    await message.answer(text, reply_markup=markup)
    
    