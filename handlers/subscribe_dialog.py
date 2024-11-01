from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.filters.command import Command
import logging


from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Back, Select, Group, Multiselect
from aiogram_dialog.widgets.text import Const, Format


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
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


async def window1_get_data(
    session: AsyncSession, dialog_manager: DialogManager, **kwargs
):
    print("window1_get_data")
    query = select(
        Main_cathegories.main_cathegory_name, Main_cathegories.main_cathegory_id
    )
    response = await session.execute(query)
    result = response.all()

    user_id = dialog_manager.event.from_user.id

    check_query = select(Subscriptions.cathegory_id).where(
        Subscriptions.user_id == user_id
    )
    check_response = await session.execute(check_query)
    users_subscriptions = check_response.all()

    users_subscriptions = [i[0] for i in users_subscriptions]

    multiselect = dialog_manager.find("sub")
    for category_id in users_subscriptions:
        await multiselect.set_checked(category_id, True)


    return {
        "main_cathegories": result,
    }


async def window2_get_data(session: AsyncSession, dialog_manager: DialogManager, **kwargs):
    print("window2_get_data")
    main_cath = dialog_manager.dialog_data["main_cath"]
    main_cath = int(main_cath)
    query = select(
        Subcathegories.subcathegory_name, Subcathegories.subcathegory_id
        ).where(Subcathegories.main_cathegory_id == main_cath)
    
    response = await session.execute(query)
    result = response.all()

    return {"subcathegories": result}


async def button1_clicked(
    callback: CallbackQuery,
    session: AsyncSession,
    dialog_manager: DialogManager,
    data: Optional[dict],
):
    user_id = callback.from_user.id

    main_cath = dialog_manager.event.data.split(":")[1]
    dialog_manager.dialog_data["main_cath"] = main_cath
    dialog_manager.dialog_data["user_id"] = user_id

    await dialog_manager.next()


async def delete_sub(session: AsyncSession, user_id, cathegory_id):
    print("delete_sub")
    user_id = int(user_id)
    cathegory_id = int(cathegory_id)
    query = (delete(Subscriptions).where(
        and_(
            Subscriptions.user_id == user_id, Subscriptions.cathegory_id == cathegory_id
        )
    ))
    try:
        await session.execute(query)
        await session.commit()
    except Exception as e:
        logging.error(e)


async def add_sub(session: Optional[AsyncSession], user_id, cathegory_id):
    user_id = int(user_id)
    cathegory_id = int(cathegory_id)
    insert_query = (insert(Subscriptions).values(user_id=user_id, cathegory_id=cathegory_id))

    try:
        await session.execute(insert_query)
        await session.commit()
        print('inserted')
    except Exception as e:
        print(e)
        logging.error(e)


async def button2_clicked(
    callback: CallbackQuery,
    session: AsyncSession,
    dialog_manager: DialogManager,
    data: Optional[dict],
):
    from database.engine import session_maker
    category_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    multiselect = dialog_manager.find("sub")
    
    cathegory_id = int(category_id)
    if multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, True)
        async with session_maker() as session:

            await delete_sub(session, user_id=user_id, cathegory_id=cathegory_id)

    if not multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, False)
        async with session_maker() as session:
            await add_sub(session, user_id=user_id, cathegory_id=cathegory_id)

    


sel1 = Select(
    Format("{item[0]}"),
    id="main",
    item_id_getter=operator.itemgetter(1),
    items="main_cathegories",
    on_click=button1_clicked,
)
multi1 = Multiselect(
    Format("✅ {item[0]}"),
    Format("☑️{item[0]}"),
    id="sub",
    item_id_getter=operator.itemgetter(1),
    items="subcathegories",
    on_click=button2_clicked,
)


dialog = Dialog(
    Window(
        Format(
            "Добро пожаловать в бота!\nДля проверки своих подписок нажмите на команду /subscribe"
        ),
        Group(sel1, width=1),
        state=MySG.window1,
        getter=window1_get_data,  # here we specify data getter for window1
    ),
    Window(
        Format("Выберите подкатегории"),
        Group(multi1, width=1),
        Back(text=Const("⏪назад")),
        state=MySG.window2,
        getter=window2_get_data,  # here we specify data getter for window2
    ),
    getter=dialog_get_data,  # here we specify data getter for dialog
)


@router.message(Command("subscribe"), F.chat.type == "private")
async def handle_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)
