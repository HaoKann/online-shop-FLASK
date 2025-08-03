from flask import Flask, session, request
from app.config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session

# Создаем экземпляр CSRF-защиты
csrf = CSRFProtect()

app = Flask(__name__, template_folder='templates')

app.config.from_object(Config)

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для получения доступа'

Session(app)

# Инициализируем для приложения
csrf.init_app(app)


# Подключение платежки Stripe
# 1. Импортируем сам blueprint (payment_bp) из файла payment.py
from app.payment import payment_bp

# 2. Регистрируем его в приложении
app.register_blueprint(payment_bp)

# Передача CSRF-токена в шаблоны
@app.context_processor
def inject_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = csrf._get_csrf_token(request) # Генерация токена
    return {'csrf_token': session.get('csrf_token')}



from app.controllers import main_controller, catalog_controller, pc_help_controller, promotions_controller, \
ready_pc_controller, user_controller, user_orders_controller, favourites_controller,cart_controller, \
auth_controller, search_controller, theme_controller
from app.controllers.admin import admin_controller
from app.models import cart, order, product, user, about
