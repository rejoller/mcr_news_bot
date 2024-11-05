from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

from icecream import ic


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        logging.info(f"Received message from {event.from_user.id}: {event.text}")
        return await handler(event, data)
