from aiogram import Router, F, flags
from aiogram.types import  Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from database.models import Subscriptions, Subcategories, Messages
from icecream import ic
import imaplib
from email.header import decode_header
from email import message_from_bytes
import asyncio
import os
from config import IMAP_SERVER, EMAIL, PASSWORD, SAVE_DIR
import logging



router = Router()



async def fetch_email_by_id(EMAIL_ID):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    await asyncio.to_thread(mail.login, EMAIL, PASSWORD)
    await asyncio.to_thread(mail.select, 'inbox')

    result, data = await asyncio.to_thread(mail.search, None, f'HEADER Message-ID "{EMAIL_ID}"')
    
    if result == 'OK' and data[0]:  
        email_nums = data[0].split()
        num = email_nums[-1] 
        result, email_data = await asyncio.to_thread(mail.fetch, num, '(RFC822)')
        raw_email = email_data[0][1]
        
        print("Email found:", raw_email)
    else:
        print("Email not found with the specified Message-ID.")

    mail.logout()
    return message_from_bytes(raw_email)


def decode_file_name(encoded_name):
        d_header = decode_header(encoded_name)[0]
        if isinstance(d_header[0], bytes):
            return d_header[0].decode(d_header[1] or 'utf8')
        return d_header[0]


async def msg_saver(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    filename = decode_file_name(filename)
                    filepath = os.path.join(SAVE_DIR, filename)
                    
                    with open(filepath, 'wb') as file:
                        file.write(part.get_payload(decode=True))
                        if os.path.exists(filepath):
                            logging.info(f"File {filename} saved successfully.")
                            return filepath



@router.callback_query(F.data.startswith("msgcat"))
async def last_news(call: CallbackQuery, session: AsyncSession, flags = {"long_operation":"typing"}):
    cat_id = call.data.split(":")[1]
    query = select(Messages.email_id).where(Messages.subcategory_id == int(cat_id[0])).order_by(Messages.date_send.desc()).limit(1)
    response = await session.execute(query)
    result = response.all()
    email_id = result[0][0] if result else None
    if not email_id:
        await call.answer("Отсутствуют материалы для отправки", show_alert=True)
        return
    
    
    
    await call.answer("Отправляю материал")
    msg = await fetch_email_by_id(email_id)
    img_path = await msg_saver(msg)
    if img_path:
        await call.message.answer_photo(photo=FSInputFile(img_path))
        await call.answer()
        if os.path.exists(img_path):
            os.remove(img_path)
    else:
        await call.answer("Возникла ошибка при отправке", show_alert=True)
    