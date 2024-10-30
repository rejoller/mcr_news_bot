from aiogram_dialog import (
    Dialog, DialogManager,
    setup_dialogs, StartMode, Window,
)
import operator
import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message


from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Multiselect, Start
from aiogram_dialog.widgets.text import Const, Format

from datetime import datetime
from icecream import ic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.dialects.postgresql import insert

from database.models import News_cathegories, Subscriptions



class DialogSG(StatesGroup):
    greeting = State()


async def get_data(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    print('get_data')
    
    user_id = dialog_manager.event.from_user.id
    data = dialog_manager.event.data
    ic(data)
    
    context = dialog_manager.current_context()
    
    if data:
        data = data.split(':')[1]
        ic(data)
        to_widget = []
        to_widget = data,
        for i in to_widget:
            context.widget_data.update({'sub': i})
        
        subquery = select(News_cathegories.cathegory_id).where(News_cathegories.cathegory_name == data)
        result = await session.execute(subquery)
        cathegory_id = int(result.first()[0])
        
        ic(cathegory_id)
        
    
        
        check_query = select(Subscriptions.cathegory_id).where(and_(Subscriptions.user_id == user_id, Subscriptions.cathegory_id == cathegory_id))
        result = await session.execute(check_query)
        response = result.all()
        result = [(i[0]) for i in response]
        
        ic(result)
        
        if cathegory_id in result:
            delete_query = delete(Subscriptions).where(and_(Subscriptions.cathegory_id == cathegory_id, Subscriptions.user_id == user_id))
            try:
                await session.execute(delete_query)
                await session.commit()
                print('deleted')
            except Exception as e:
                logging.error(e)
                
        else:
            insert_query = insert(Subscriptions).values(
                user_id=user_id,
                cathegory_id=cathegory_id
            )
            try:
                await session.execute(insert_query)
                await session.commit()
                print('inserted')
            except Exception as e:
                logging.error(e)
            
        

    
    check_query = select(News_cathegories.cathegory_name) \
                    .join(Subscriptions, and_(Subscriptions.cathegory_id == News_cathegories.cathegory_id,
                    Subscriptions.user_id == user_id))
    result = await session.execute(check_query)
    response = result.all()
    result = [(i[0]) for i in response]
    
    to_widget = []
    to_widget = result,
    for i in to_widget:
        context.widget_data.update({'sub': i})
    
    
    
                    
    query = select(News_cathegories.cathegory_id, News_cathegories.cathegory_name)
                    
    result = await session.execute(query)
    response = result.all()
    
    result = [(i[1]) for i in response]
   
    
    

    context.start_data = result
    
    
    
    
            
    user_subscriptions = context.start_data

    
    
    return {

        "user_subscriptions": user_subscriptions
    }
    


async def name_handler(
        message: Message, message_input: MessageInput, manager: DialogManager,
):
    print('name_handler')
    manager.dialog_data["last_text"] = message.text
    await message.answer(f"Nice to meet you, {message.text}")


async def on_click(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    print('on_click')

    counter = manager.dialog_data.get("counter", 0)

    manager.dialog_data["counter"] = counter + 1
    
    context = manager.current_context()
    ic(context)


multi = Multiselect(
    Format("✓ {item}"),  
    Format("{item}"),
    id="sub",
    item_id_getter = lambda x: x,
    items="user_subscriptions",
)

dialog = Dialog(
    Window(
        Const("Choose cathegory"),

        multi,
        Cancel(),
        # Inputs work only in default stack
        # or via reply to a message with buttons
        MessageInput(name_handler),
        state=DialogSG.greeting,
        getter=get_data,
    ),
)

# async def start(message: Message, session: AsyncSession, dialog_manager: DialogManager):
#     print('start')
#     await dialog_manager.start(DialogSG.greeting, mode=StartMode.NEW_STACK)
    
    
    
