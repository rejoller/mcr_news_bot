import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database.models import Main_cathegories, Subscriptions
from icecream import ic
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards.choise_subcath import DialogSG




router=Router()




@router.callback_query(F.data.startswith('subcath'), F.chat.type == 'private')
async def handle_subscribe(callback: CallbackQuery, state: FSMContext, dialog_manager: DialogManager, session: AsyncSession):
    await state.clear()
    ic(callback.data)
    await dialog_manager.start(DialogSG.sub_cathegories, mode=StartMode.NEW_STACK)
    print('handle_subscribe')



