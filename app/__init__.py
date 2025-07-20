from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')

app.config.from_object(Config)

bootstrap = Bootstrap5(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для получения доступа'




from app.controllers import main_controller, catalog_controller, pc_help_controller, promotions_controller, \
ready_pc_controller, user_controller, user_orders_controller, favourites_controller,cart_controller, \
auth_controller, search_controller, theme_controller

from app.controllers.admin import admin_controller
from app.models import cart, order, product, user, about