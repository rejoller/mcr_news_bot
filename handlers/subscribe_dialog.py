import logging
import operator
from typing import Optional

from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Group, Multiselect, Select
from aiogram_dialog.widgets.text import Const, Format

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Main_categories, Subcategories, Subscriptions



router = Router()

@router.message(Command("subscribe"), F.chat.type == "private", ~F.data.startswith("msgcat:"), ~F.data.startswith("airflow"), ~F.data.startswith("dag"), ~F.data.startswith("new"))
async def handle_subscribe(message: Message, dialog_manager: DialogManager):
    print('handle_subscribe')
    await dialog_manager.start(MySG.window1, mode=StartMode.NORMAL)


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
    query = select(
        Main_categories.main_category_name, Main_categories.main_category_id
    )
    response = await session.execute(query)
    result = response.all()

    user_id = dialog_manager.event.from_user.id

    check_query = select(Subscriptions.category_id).where(
        Subscriptions.user_id == user_id
    )
    check_response = await session.execute(check_query)
    users_subscriptions = check_response.all()

    users_subscriptions = [i[0] for i in users_subscriptions]

    multiselect = dialog_manager.find("sub")
    for category_id in users_subscriptions:
        await multiselect.set_checked(category_id, True)


    return {
        "main_categories": result,
    }


async def window2_get_data(session: AsyncSession, dialog_manager: DialogManager, **kwargs):
    main_cat = dialog_manager.dialog_data["main_cat"]
    main_cat = int(main_cat)
    query = select(
        Subcategories.subcategory_name, Subcategories.subcategory_id
        ).where(Subcategories.main_category_id == main_cat)
    
    response = await session.execute(query)
    result = response.all()

    return {"subcategories": result}


async def button1_clicked(
    callback: CallbackQuery,
    session: AsyncSession,
    dialog_manager: DialogManager,
    data: Optional[dict],
):
    user_id = callback.from_user.id

    main_cat = dialog_manager.event.data.split(":")[1]
    dialog_manager.dialog_data["main_cat"] = main_cat
    dialog_manager.dialog_data["user_id"] = user_id

    await dialog_manager.next()


async def delete_sub(session: AsyncSession, user_id, category_id):
    print("delete_sub")
    user_id = int(user_id)
    category_id = int(category_id)
    query = (delete(Subscriptions).where(
        and_(
            Subscriptions.user_id == user_id, Subscriptions.category_id == category_id
        )
    ))
    try:
        await session.execute(query)
        await session.commit()
    except Exception as e:
        logging.error(e)


async def add_sub(session: Optional[AsyncSession], user_id, category_id):
    user_id = int(user_id)
    category_id = int(category_id)
    insert_query = (insert(Subscriptions).values(user_id=user_id, category_id=category_id))

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
    
    category_id = int(category_id)
    if multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, True)
        async with session_maker() as session:

            await delete_sub(session, user_id=user_id, category_id=category_id)

    if not multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, False)
        async with session_maker() as session:
            await add_sub(session, user_id=user_id, category_id=category_id)

    


sel1 = Select(
    Format("{item[0]}"),
    id="main",
    item_id_getter=operator.itemgetter(1),
    items="main_categories",
    on_click=button1_clicked,
)
multi1 = Multiselect(
    Format("✅ {item[0]}"),
    Format("☑️{item[0]}"),
    id="sub",
    item_id_getter=operator.itemgetter(1),
    items="subcategories",
    on_click=button2_clicked,
)


dialog = Dialog(
    Window(
        Format(
            "Выберите интересующие категории"
        ),
        Group(sel1, width=1),
        state=MySG.window1,
        getter=window1_get_data,  
    ),
    Window(
        Format("Выберите подкатегории для оформления подписки"),
        Group(multi1, width=1),
        Back(text=Const("⏪назад")),
        state=MySG.window2,
        getter=window2_get_data, 
    ),
    getter=dialog_get_data,
    name = "subscribe"
)


