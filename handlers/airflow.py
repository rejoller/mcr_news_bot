from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession


from filters.admins import AdminFilter
from icecream import ic
from kb.show_dags import markup

router = Router()



@router.message(Command('airflow'), F.chat.type == "private")
async def handle_start(message: Message, session: AsyncSession):
    
    
    await message.answer("Airflow", reply_markup=markup)

    
    