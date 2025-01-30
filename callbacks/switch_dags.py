from aiogram import Router, F, Bot
from aiogram.types import  CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime
import requests
from icecream import ic


import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession


from filters.admins import CallbackQueryAdminFilter
from config import HOST_AIRFLOW, USER_AIRFLOW, PASSWORD_AIRFLOW, DAG_ID
from kb.show_dags import markup
import logging


router = Router()


@router.callback_query(F.data.startswith("dagswitch"), CallbackQueryAdminFilter())
async def switch_dags(call: CallbackQuery, session: AsyncSession, bot: Bot):
    dag_id = call.data.split(':')[1]
    res = requests.get(url=f'{HOST_AIRFLOW}/api/v1/dags', 
                            headers={'Content-Type': 'application/json', 
                                    'Accept': 'application/json'}, 
                            auth=(USER_AIRFLOW, PASSWORD_AIRFLOW))
    res_json = res.json()
    for dag in enumerate(res_json['dags']):
    
        if dag[1]['dag_id'] == dag_id and not dag[1]['is_paused']:
            try:
                response = requests.patch(url=f'{HOST_AIRFLOW}/api/v1/dags/{DAG_ID}?update_mask=is_paused',headers={'Content-Type': 'application/json'}, auth=(USER_AIRFLOW, PASSWORD_AIRFLOW), json={'is_paused': True})
                if response.ok:
                    
                    try:
                        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                    except Exception as e:
                        logging.error(f'Ошибка удаления сообщения {call.message.message_id}: ', e)
                        
                    await call.message.answer(f'DAG {dag_id} поставлен на паузу', reply_markup=markup)
                    await call.answer()
                else: 
                    await call.message.answer(f'Ошибка {response.status_code}')
                    await call.answer()
            except Exception as e:
                logging.error('Ошибка с airflow: ', e)
                    
                    
        if dag[1]['dag_id'] == dag_id and dag[1]['is_paused']:
            try:
                response = requests.patch(url=f'{HOST_AIRFLOW}/api/v1/dags/{DAG_ID}?update_mask=is_paused',headers={'Content-Type': 'application/json'}, auth=(USER_AIRFLOW, PASSWORD_AIRFLOW), json={'is_paused': False})
                if response.ok:
                    await call.message.answer(f'DAG {dag_id} снят с паузы', reply_markup=markup)
                    try:
                        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                    except Exception as e:
                        logging.error(f'Ошибка удаления сообщения {call.message.message_id}: ', e)
                        
                    await call.answer()
                else: 
                    await call.message.answer(f'Ошибка {response.status_code}')
                    await call.answer()
            except Exception as e:
                logging.error('Ошибка с airflow: ', e)
        
            
