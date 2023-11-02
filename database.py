import sqlite3
from datetime import datetime
import pytz

DATABASE_NAME = "my_bot_database.db"

def connect_to_db() -> sqlite3.Connection:
    return sqlite3.connect(DATABASE_NAME)

def get_current_krasnoyarsk_time():
    krasnoyarsk_timezone = pytz.timezone('Asia/Krasnoyarsk')
    return datetime.now(krasnoyarsk_timezone).strftime('%Y-%m-%d %H:%M:%S')

def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Создание таблицы subscribers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscribers (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        date_of_sub TEXT
    )
    ''')

    # Создание таблицы messages
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id TEXT PRIMARY KEY,
        date_of_sending TEXT,
        user_id INTEGER NOT NULL,
        delivered BOOLEAN,
        FOREIGN KEY(user_id) REFERENCES subscribers(user_id)
    )
    ''')

    conn.commit()
    conn.close()

def check_subscriber_exists(user_id: int) -> bool:
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subscribers WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return bool(data)

def get_all_subscriber_ids():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM subscribers")
    rows = cursor.fetchall()
    conn.close()
    
    # Извлечение user_id из каждой строки и преобразование в список
    subscriber_ids = [row[0] for row in rows]
    
    return subscriber_ids


    
def add_subscriber(user_id: int, first_name: str, last_name: str):
    if check_subscriber_exists(user_id):
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscribers (user_id, first_name, last_name, date_of_sub) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, get_current_krasnoyarsk_time()))
    conn.commit()
    conn.close()

def remove_subscriber(user_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscribers WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

    
def add_message(user_id: int, delivered: bool):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (date_of_sending, user_id, delivered) VALUES (?, ?, ?)", (get_current_krasnoyarsk_time(), user_id, delivered))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
