import requests
from flask import current_app

def send_telegram_message(message):
    """
    Отправляет сообщение в Telegram указанному чату.
    """
    # Эти данные лучше хранить в конфиге, но пока пропишем здесь для старта
    # Замените на свои значения!
    BOT_TOKEN = "8331557770:AAHQzwgLTgN_IevkSgumiMoQkGrpcchE7hU"
    CHAT_ID = "1242045637"

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram token or Chat ID not set")
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