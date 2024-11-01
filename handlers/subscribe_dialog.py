from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.filters.command import Command



from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Back, Select, Group, Multiselect
from aiogram_dialog.widgets.text import Const, Format



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.models import Main_cathegories, Subscriptions, Subcathegories


from icecream import ic
import operator
from typing import Optional



router = Router()


class MySG(StatesGroup):
    window1 = State()
    window2 = State()
    
    
async def dialog_get_data(**kwargs):
    return {
        "name": "Tishka17",
    }






async def window1_get_data(session: AsyncSession,**kwargs):
    print('window1_get_data')
    query = select(Main_cathegories.main_cathegory_name, Main_cathegories.main_cathegory_id)
    response = await session.execute(query)
    result = response.all()
    ic(result)
    return {
        "main_cathegories": result,
    }


async def window2_get_data(session: AsyncSession, dialog_manager: DialogManager, **kwargs):
    print('window2_get_data')
    main_cath = dialog_manager.dialog_data['main_cath']
    main_cath = int(main_cath)
    ic(main_cath)
    
    query = select(Subcathegories.subcathegory_name, Subcathegories.subcathegory_id).where(Subcathegories.main_cathegory_id ==main_cath)
    response = await session.execute(query)
    result = response.all()
    ic(result)
    
    return {
        "subcathegories": result,
    }





async def button1_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, data: Optional[dict]):
    ic(dialog_manager.event.data)
    main_cath = dialog_manager.event.data.split(':')[1]
    ic(main_cath)
    dialog_manager.dialog_data['main_cath'] = main_cath
    await dialog_manager.next()
    
    
async def button2_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, data: Optional[dict]):
    ic(dialog_manager.event.data)
    # main_cath = manager.event.data.split(':')[1]
    # ic(main_cath)
    # manager.dialog_data['main_cath'] = main_cath
    await dialog_manager.next()


sel1=Select(Format("{item[0]}"), id="main", item_id_getter=operator.itemgetter(1), items="main_cathegories", on_click=button1_clicked)
multi1=Multiselect(Format("{item[0]}"), Format("✅ {item[0]}"), id="sub", item_id_getter=operator.itemgetter(1), items="subcathegories", on_click=button2_clicked)



dialog = Dialog(
    Window(
        Format("Добро пожаловать в бота!\nДля проверки своих подписок нажмите на команду /subscribe"),
        Group(sel1, width=1),
        Button(Const("Next window"), id="button1", on_click=button1_clicked),
        state=MySG.window1,
        getter=window1_get_data,  # here we specify data getter for window1
    ),
    Window(
        Format("Выбранная категория!"),
        Group(multi1, width=1),
        Back(text=Const("Back")),
        state=MySG.window2,
        getter=window2_get_data,  # here we specify data getter for window2
    ),
    getter=dialog_get_data  # here we specify data getter for dialog
)

@router.message(Command('subscribe'), F.chat.type == "private")
async def handle_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)