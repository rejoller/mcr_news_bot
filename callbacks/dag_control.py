from aiogram import Router, F, Bot
from aiogram.types import  CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime
import requests
from icecream import ic
import logging


import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession


from filters.admins import CallbackQueryAdminFilter
from config import HOST_AIRFLOW, USER_AIRFLOW, PASSWORD_AIRFLOW, DAG_ID



router = Router()


@router.callback_query(F.data =="dag_info", CallbackQueryAdminFilter())
async def get_dags(call: CallbackQuery, session: AsyncSession, bot: Bot):
    try:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    except Exception as e:
        logging.error(f'Ошибка удаления сообщения {call.message.message_id}: ', e)
    
    
    builder = InlineKeyboardBuilder()
    news_dag = None
    res = requests.get(url=f'{HOST_AIRFLOW}/api/v1/dags', 
                            headers={'Content-Type': 'application/json', 
                                    'Accept': 'application/json'}, 
                            auth=(USER_AIRFLOW, PASSWORD_AIRFLOW))
    res_json = res.json()
    for dag in enumerate(res_json['dags']):
    
        if dag[1]['dag_id'] == DAG_ID:
            news_dag = dag[1]
            
            
            
            
    params = {
        "limit": 1,
        "order_by": "-start_date",
    }
    last_run = requests.get(url=f'{HOST_AIRFLOW}/api/v1/dags/{DAG_ID}/dagRuns', 
                            headers={'Content-Type': 'application/json', 
                                    'Accept': 'application/json'}, 
                            auth=('kazakov.va', 'dMpsur7XTFhU'), params=params)
    last_run_json = last_run.json()
    last_run_id = last_run_json['dag_runs'][0]['dag_run_id']
    
    last_run_state = last_run_json['dag_runs'][0]['state']
    
    
    
    
    
    
    if last_run_state == 'running':
        builder.button(text="❌Прервать выполнение", callback_data=f'setfail:{last_run_id}')
        
    
        
    
    text = ''
    is_paused = ''
    owners = [i for i in news_dag['owners']]
    users = ', '.join(owners)
    
    
    
    if news_dag:
        
        
        time_ = pd.to_datetime(news_dag['next_dagrun_create_after'], utc=True).tz_convert("Asia/Krasnoyarsk")
        next_dagrun = datetime.strftime(time_, "%d.%m.%y %H:%M")
        dag_id = news_dag['dag_id']
        last_run_date = ''
        
        if not news_dag['is_paused']:
            last_run_date = pd.to_datetime(last_run_json['dag_runs'][0]['last_scheduling_decision'], utc=True).tz_convert("Asia/Krasnoyarsk")
            last_run_date = datetime.strftime(last_run_date, "%d.%m.%y %H:%M")
            is_paused = '▶️включен'
            builder.button(text = "⏸️Пауза", callback_data=f"dagswitch:{dag_id}")
            if last_run_state != 'running':
                if last_run_state == 'failed':
                    last_run_state = 'failed🔴'
                builder.button(text="Выполнить DAG", callback_data=f'newrun:{DAG_ID}')
        else:
            is_paused = '⏸️на паузе'
            builder.button(text = "⏸️снять DAG с паузы", callback_data=f"dagswitch:{dag_id}")
            
        
            
        text += f'({is_paused})<b> {news_dag['dag_display_name']}</b>\n'
        text += f'<b>Описание: </b> {news_dag['description']} \n'
        text += f'<b>Владельцы: </b> {users}\n\n'
        if last_run_state != 'running':
            text += "<b>Статус: </b> 🕙Ждет запуска\n"
            text += f'<b>Последнее выполнение: </b> {last_run_date} (статус {last_run_state})\n'
        else:
            text += 'DAG выполняется🟡\n'
        text += f'<b>Следующий запуск: </b> {next_dagrun}'

        
        markup = builder.as_markup()
        
        msg_tg = await call.message.answer(text=text, reply_markup=markup, parse_mode='HTML')


        await call.answer()
        
        
        
        
        
    