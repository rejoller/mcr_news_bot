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
from kb.show_dags import markup



import json



router = Router()

@router.callback_query(F.data.startswith("setfail"), CallbackQueryAdminFilter())
async def get_dags(call: CallbackQuery, session: AsyncSession, bot: Bot):

    
    params = {
        "limit": 1,
        "order_by": "-start_date",
    }
    res = requests.get(url=f'{HOST_AIRFLOW}/api/v1/dags/{DAG_ID}/dagRuns', 
                            headers={'Content-Type': 'application/json', 
                                    'Accept': 'application/json'}, 
                            auth=('kazakov.va', 'dMpsur7XTFhU'), params=params)
    res_json = res.json()

    dag_run_id = res_json['dag_runs'][0]['dag_run_id']

    body = {
    "state": "failed",
    }
    edit = requests.patch(url=f'{HOST_AIRFLOW}/api/v1/dags/{DAG_ID}/dagRuns/{dag_run_id}', 
                            headers={'Content-Type': 'application/json'}, data=json.dumps(body),
                            auth=('kazakov.va', 'dMpsur7XTFhU'))
    if edit.ok:
        try:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        except Exception as e:
            logging.error(f'Ошибка удаления сообщения {call.message.message_id}: ', e)
            
        await call.message.answer(f'Выполнение DAG {DAG_ID} прервано', reply_markup=markup)
    else:
        await call.answer('Возникла ошибка😳')