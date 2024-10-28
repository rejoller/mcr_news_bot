from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import CommandStart





router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def handle_start(message: Message):
    await message.answer("Добро пожаловать в бота")