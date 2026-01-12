import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из файла .flaskenv
load_dotenv()

def send_telegram_message(message):
    """
    Отправляет сообщение в Telegram указанному чату.
    """
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        print("Ошибка: Токен или ID не найдены")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # Позволяет использовать жирный текст и ссылки
    }

    try: 
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            print(f"Ошибка отправки в Telegram: {response.text}")
    except Exception as e:
        print(f'Ошибка соединения с Telegram: {e}')