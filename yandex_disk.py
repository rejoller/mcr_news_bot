import os
import sqlite3
import imaplib
from email import message_from_bytes
from email.header import decode_header
from datetime import datetime, timedelta
from database import add_subscriber, add_message, check_subscriber_exists, remove_subscriber

# Подключаемся к базе данных
conn = sqlite3.connect("my_bot_database.db")
cursor = conn.cursor()

SAVE_DIR = './saved_files'
EMAIL_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'

def fetch_and_save_files(user_id: int):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    def decode_file_name(encoded_name):
        d_header = decode_header(encoded_name)[0]
        if isinstance(d_header[0], bytes):
            return d_header[0].decode(d_header[1] or 'utf8')
        return d_header[0]

    def save_file(part, filename):
        with open(os.path.join(SAVE_DIR, filename), 'wb') as file:
            file.write(part.get_payload(decode=True))

    mail = imaplib.IMAP4_SSL('imap.rambler.ru')
    mail.login('shawnrosales5v@rambler.ru', 'Av9505047@@')
    mail.select('inbox')

    saved_files = []

    result, data = mail.search(None, 'ALL')
    emails = []
    for num in data[0].split():
        result, email_data = mail.fetch(num, '(RFC822)')
        raw_email = email_data[0][1]
        msg = message_from_bytes(raw_email)
        emails.append(msg)

    # Обрабатываем только последнее сообщение
    if emails:
        msg = emails[-1]

        # Проверяем, было ли это письмо уже отправлено
        email_id = msg["Message-ID"]
        print(type(email_id))

        cursor.execute("SELECT * FROM messages WHERE message_id=?", (email_id,))
        if cursor.fetchone():
            return []

        cursor.execute("INSERT INTO messages(message_id, user_id) VALUES(?, ?)", (email_id, user_id))
        conn.commit()
        add_message(user_id, False)  # False или True в зависимости от статуса delivered


        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        filename = decode_file_name(filename)
                        save_file(part, filename)
                        saved_files.append(os.path.join(SAVE_DIR, filename))

    mail.logout()
    return saved_files





