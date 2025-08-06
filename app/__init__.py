from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



# Создаем экземпляры расширений ГЛОБАЛЬНО, но не инициализируем их
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap5()


login_manager.login_view = 'auth_controller.login'
login_manager.login_message = 'Войдите в аккаунт для получения доступа'


def create_app(config_class=Config):
    # Это фабрика приложений
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализируем расширения внутри фабрики
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)


    # --- РЕГИСТРАЦИЯ BLUEPRINTS ---
    # Подключение платежки Stripe
    # 1. Импортируем сам blueprint (payment_bp) из файла payment.py
    from .payment import payment_bp
    # 2. Регистрируем его в приложении
    app.register_blueprint(payment_bp)

    # РЕГИСТРИРУЕМ BLUEPRINT для главной страницы
    from .controllers.main_controller import main_bp
    app.register_blueprint(main_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ catalog_bp
    from .controllers.catalog_controller import catalog_bp
    app.register_blueprint(catalog_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ pc_help_bp
    from .controllers.pc_help_controller import pc_help_bp
    app.register_blueprint(pc_help_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ promotions_bp
    from .controllers.promotions_controller import promotions_bp
    app.register_blueprint(promotions_bp)

    from .controllers import ready_pc_controller, user_controller, user_orders_controller, favourites_controller,cart_controller, \
    auth_controller, search_controller, theme_controller
    from app.controllers.admin import admin_controller
    from app.models import cart, order, product, user, about

    return app
