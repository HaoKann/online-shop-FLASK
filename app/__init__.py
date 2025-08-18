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

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ ready_pc_bp
    from .controllers.ready_pc_controller import ready_pc_bp
    app.register_blueprint(ready_pc_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ user_bp
    from .controllers.user_controller import user_bp
    app.register_blueprint(user_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ user_order_bp
    from .controllers.user_orders_controller import user_order_bp
    app.register_blueprint(user_order_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ favourites_bp
    from .controllers.favourites_controller import favourites_bp
    app.register_blueprint(favourites_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ cart_bp
    from .controllers.cart_controller import cart_bp
    app.register_blueprint(cart_bp)
    
    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ ДЛЯ auth_bp
    from .controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ search_bp
    from .controllers.search_controller import search_bp
    app.register_blueprint(search_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ theme_bp
    from .controllers.theme_controller import theme_bp
    app.register_blueprint(theme_bp)

    # ДОБАВЛЯЕМ РЕГИСТРАЦИЮ theme_bp
    from .controllers.admin.admin_controller import admin_bp
    app.register_blueprint(admin_bp)

    from app.controllers.admin import admin_controller
    from app.models import cart, order, product, user, about

    return app
