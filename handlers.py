from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from yandex_disk import fetch_and_save_files
import fitz
import tempfile
from aiogram.types import FSInputFile, InputFile
from bot import router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import start_keyboard
from database import add_subscriber, add_message, check_subscriber_exists, remove_subscriber
from message_sender import send_files_to_user



'''
@router.message(F.text)
async def handle_all_messages(message: types.Message):
    await message.answer("Я получил ваше сообщение!")
'''

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Хотите подписаться на рассылку новостей?", reply_markup=start_keyboard())


@router.callback_query(lambda c: c.data == 'subscribe')
async def subscribe_user(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    last_name = callback_query.from_user.last_name

    if check_subscriber_exists(user_id):
        await callback_query.answer("Вы уже являетесь подписчиком!")
    else:
        add_subscriber(user_id, first_name, last_name)
        await callback_query.answer("Вы успешно подписались на рассылку!")
        files = fetch_and_save_files(user_id)
        print(f"Fetched files: {files}")
        await send_files_to_user(callback_query.message, files)
        

@router.message(Command("unsub"))
async def unsubscribe_user(message: types.Message):
    user_id = message.from_user.id

    if check_subscriber_exists(user_id):
        remove_subscriber(user_id)
        await message.answer("Вы успешно отписались от рассылки!")
    else:
        await message.answer("Вы не являетесь подписчиком!")
        
'''
def convert_pdf_to_images(pdf_path):
    """Конвертирует PDF в список имен временных файлов."""
    doc = fitz.open(pdf_path)
    temp_files = []
    for page in doc:
        pix = page.get_pixmap()
        temp_file_name = tempfile.mktemp(suffix=".png")
        pix.save(temp_file_name)
        temp_files.append(temp_file_name)
    return temp_files
'''
