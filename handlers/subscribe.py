import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database.models import News_cathegories, Subscriptions
from icecream import ic
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards.choise_cath import DialogSG




router=Router()




@router.message(Command('subscribe'), F.chat.type == 'private')
async def handle_subscribe(message: Message, state: FSMContext, dialog_manager: DialogManager, session: AsyncSession):
    await state.clear()
    await dialog_manager.start(DialogSG.greeting, mode=StartMode.NEW_STACK)
    print('handle_subscribe')
    # user_id = message.from_user.id

    # query = select(News_cathegories.cathegory_id, News_cathegories.cathegory_short_name, News_cathegories.cathegory_name, News_cathegories.cathegory_description)
    # result = await session.execute(query)
    # all_cathegories = result.all()
    
    
    # ic(all_cathegories)
    
    # builder = InlineKeyboardBuilder()
    
    # for id in all_cathegories:
    #     ic(id[0], id[1], id[2], id[3])
    #     builder.button(text = id[2], callback_data=f'subscribe_{id[0]}_{id[2]}')
    
    # builder.adjust(1)
    
    # keyboard = builder.as_markup()
    # try:
    #     await message.answer('Выберите категорию', reply_markup=keyboard)
    # except Exception as e:
    #     logging.error(e)
