from aiogram import types
from aiogram.types import InputFile
from aiogram.types.input_file import FSInputFile
import fitz
import tempfile



from aiogram import Bot, Router, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


BOT_TOKEN  = '6569068360:AAEUN1C31L78AAFwuztKdrM4q5xyeHBSuyk'
bot = Bot(token=BOT_TOKEN)

router = Router()

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)



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




async def send_files_to_user(user_id: int, files):
    for file_path in files:
        if file_path.endswith(('.png', '.jpg', '.jpeg')):
            await bot.send_photo(chat_id=user_id, photo=FSInputFile(file_path))
        elif file_path.endswith('.pdf'):
            temp_files = convert_pdf_to_images(file_path)
            for temp_file in temp_files:
                await bot.send_photo(chat_id=user_id, photo=FSInputFile(path=temp_file, filename="image.png"))
        else:
            with open(file_path, 'rb') as file:
                await bot.send_document(chat_id=user_id, document=InputFile(data=file.read(), filename=file_path.split('/')[-1]))
