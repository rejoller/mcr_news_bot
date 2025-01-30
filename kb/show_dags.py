from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



text = 'посмотреть информацию о DAG'

markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text, callback_data='dag_info')
    ]
])