from aiogram_dialog import (
    Dialog, DialogManager,
    setup_dialogs, StartMode, Window,
)
import operator
import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message


from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Multiselect, Group
from aiogram_dialog.widgets.text import Const, Format


from datetime import datetime
from icecream import ic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.dialects.postgresql import insert

from database.models import Main_cathegories, Subscriptions, Subcathegories



class DialogSG(StatesGroup):
    sub_cathegories = State()


async def get_data(dialog_manager: DialogManager, session: AsyncSession, **kwargs):
    print('get_data')
    
    user_id = dialog_manager.event.from_user.id
    data = dialog_manager.event.data
    ic(data)
    
    context = dialog_manager.current_context()
    if data and len(data.split(':')) == 3:
        data = data.split(':')[2]
        
        
        subquery = select(Subcathegories.subcathegory_name, Subcathegories.subcathegory_id).where(Subcathegories.main_cathegory_id == int(data[0]))
        result = await session.execute(subquery)
        cathegories = result.all()
        cathegories_name = [i[0] for i in cathegories]
        
        cathegories_id = [i[1] for i in cathegories]
        
        
        
        
        to_widget = []
        to_widget = cathegories_name,
        for i in to_widget:
            context.widget_data.update({'sub': i})
        
        ic(context)
        
        for id in cathegories_id:
            check_query = select(Subscriptions.cathegory_id).where(and_(Subscriptions.user_id == user_id, Subscriptions.cathegory_id == id))
        result = await session.execute(check_query)
        response = result.all()
        ic(response)
        result = [(i[0]) for i in response]
        
        ic(result)
        
        if cathegories_id in result:
            try:
                for id in cathegories_id:
                    delete_query = delete(Subscriptions).where(and_(Subscriptions.cathegory_id == id, Subscriptions.user_id == user_id))

                    await session.execute(delete_query)
                await session.commit()
                print('deleted')
            except Exception as e:
                logging.error(e)

                
        else:
            try:
                for id in cathegories_id:
                    insert_query = insert(Subscriptions).values(
                        user_id=user_id,
                        cathegory_id=id
                    ).on_conflict_do_nothing()
                    await session.execute(insert_query)
                await session.commit()
                await session.close()
                print('inserted')
            except Exception as e:
                logging.error(e)

                
                
                

            
    check_query = select(Subcathegories.subcathegory_name) \
                    .join(Subscriptions, and_(Subscriptions.cathegory_id == Subcathegories.subcathegory_id,
                    Subscriptions.user_id == user_id))
    result = await session.execute(check_query)
    response = result.all()
    result = [(i[0]) for i in response]
    ic('107', result)
    
    to_widget = []
    to_widget = result,
    for i in to_widget:
        context.widget_data.update({'sub': i})
    
    query = select(Subcathegories.subcathegory_id, Subcathegories.subcathegory_name)
                    
    result = await session.execute(query)
    response = result.all()
    result = [(i[1]) for i in response]
    context.start_data = result
           
    user_subscriptions = context.start_data

    ic(context)
    ic(user_subscriptions)
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
    Format("✅ {item}"),  
    Format("☑️{item}"),
    id="sub",
    item_id_getter = lambda x: x,
    items="user_subscriptions",
)

sub_cathegories = Dialog(
    Window(
        Const("Choose cathegory"),
        Group(multi, width=1),
        Cancel(),
        MessageInput(name_handler),
        state=DialogSG.sub_cathegories,
        getter=get_data,
    ),
)

    
    
