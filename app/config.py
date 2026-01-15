import os
from dotenv import load_dotenv

# Загружаем переменные из .flaskenv
load_dotenv()

# Находим базовую директорию проекта
basedir = os.path.abspath(os.path.dirname(__file__))

# Определяем КОРЕНЬ проекта
root_dir = os.path.dirname(basedir)

# Загружаем переменные из .flaskenv
load_dotenv(os.path.join(root_dir, '.flaskenv'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'oidsngoisdngiodsnoipngsdfopgsfd' 

    # --- ГЛАВНОЕ ИЗМЕНЕНИЕ ---
    # 1. Пытаемся взять адрес из Докера (переменная SQLALCHEMY_DATABASE_URI)
    # 2. Если её нет, берем локальный адрес (для запуска без Докера)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'postgresql+psycopg2://postgres:123456789@localhost:5432/online_shop_db'
    
    # Исправление для Render (заменяем postgres:// на postgresql://)
    if SQLALCHEMY_DATABASE_URI  and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

    # Если переменной нет (локальный запуск), используем запасной вариант
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456789@localhost:5432/online_shop_db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False    

    # Имена переменных должны совпадать с docker-compose.yml
    # В docker-compose написал STRIPE_PUBLIC_KEY, поэтому здесь ищем её же
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLIC_KEY') or os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    
    SESSION_TYPE = 'filesystem'