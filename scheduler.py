from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from yandex_disk import fetch_and_save_files
from message_sender import send_files_to_user
from database import get_all_subscriber_ids
import logging
import asyncio

logging.basicConfig(level=logging.INFO)


async def scheduled_task():
    subscriber_ids = get_all_subscriber_ids()
    for user_id in subscriber_ids:
        try:
            files = fetch_and_save_files(user_id)
            await send_files_to_user(user_id, files)
            logging.info(f"Successfully sent files to user_id: {user_id}")
            await asyncio.sleep(15)  # Pause for 15 seconds before sending to the next user
        except Exception as e:
            logging.error(f"Error sending files to user_id: {user_id}. Error: {e}")

def start_scheduler(interval_seconds=70):  # по умолчанию каждый час
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scheduled_task, 
        IntervalTrigger(seconds=interval_seconds)
    )
    scheduler.start()

