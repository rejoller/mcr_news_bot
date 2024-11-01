from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode





router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def handle_start(message: Message):
    await message.answer("Добро пожаловать в бота!\nДля проверки своих подписок нажмите на команду /subscribe")
    
    
    

    
    
