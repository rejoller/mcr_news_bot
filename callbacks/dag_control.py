from aiogram import Router, F, Bot
from aiogram.types import  CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime
import requests
from icecream import ic
import logging


import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession


from filters.admins import CallbackQueryAdminFilter
from config import HOST_AIRFLOW, USER_AIRFLOW, PASSWORD_AIRFLOW



router = Router()


@router.callback_query(F.data =="dag_info", CallbackQueryAdminFilter())
async def get_dags(call: CallbackQuery, session: AsyncSession, bot: Bot):
    ic('get_dags')
    # try:
    #     await bot.delete_message(chat_id=call.message.from_user.id, message_id=call.message.message_id-1)
    # except Exception as e:
    #     logging.error(f'Ошибка удаления сообщения {call.message.message_id-1}: ', e)
        
    news_dag = None
    res = requests.get(url=f'{HOST_AIRFLOW}/api/v1/dags', 
                            headers={'Content-Type': 'application/json', 
                                    'Accept': 'application/json'}, 
                            auth=(USER_AIRFLOW, PASSWORD_AIRFLOW))
    res_json = res.json()
    for dag in enumerate(res_json['dags']):
    
        if dag[1]['dag_display_name'] == 'cleanup_xcom':
            news_dag = dag[1]
            
    
    text = ''
    status_dag = ''
    text_button = ''
    owners = [i for i in news_dag['owners']]
    users = ', '.join(owners)
    
    
    
    if news_dag:
        time_ = pd.to_datetime(news_dag['next_dagrun'], utc=True).tz_convert("Asia/Krasnoyarsk")
        next_dagrun = datetime.strftime(time_, "%d.%m.%y %H:%M")
        dag_id = news_dag['dag_id']
        if not news_dag['is_paused']:
            status_dag = '🟢активен'
            text_button = '⏸️Пауза'
        else:
            status_dag = '🔴на паузе'
            text_button = '▶️Запуск'
            
            
        text += f'({status_dag})<b> {news_dag['dag_display_name']}</b>\n'
        text += f'<b>Описание: </b> {news_dag['description']} \n'
        text += f'<b>Владельцы: </b> {users}\n\n'
        text += f'<b>Следующий запуск: </b> {next_dagrun}'

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=text_button, callback_data=f'dagswitch:{dag_id}')
            ]
        ])
        
        await call.message.answer(text=text, reply_markup=markup, parse_mode='HTML')
        await call.answer()
        
        
        
        
        
    