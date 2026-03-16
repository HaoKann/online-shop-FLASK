import pytest
from app import create_app, db
from app.config import Config
from datetime import date
from app.models.user import User
from app.models.cart import Cart


# Создаем специальный конфиг-двойник только для тестов
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    """Настраиваем приложение через фабрику."""
    # Передаем наш безопасный конфиг прямо в фабрику!
    flask_app = create_app(config_class=TestConfig)
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app # Здесь выполняется сам тест

        # Уборка после теста
        db.session.remove()
        db.drop_all()

        # Закрываем соединение с базой
        db.engine.dispose()

@pytest.fixture
def client(app):
    """Создаем виртуальный браузер (test_client) для симуляции действий пользователя."""
    return app.test_client()


@pytest.fixture
def auth_client(client, app):
    """Создает юзера, логинится под ним и возвращает авторизованный клиент."""

    with app.app_context():
        # 1. Создаем пользователя
        user = User(
            name='Тестовый покупатель',
            nickname='test_buyer',
            email='test_buyer@mail.ru',
            date_of_birth=date(1990, 1, 1)
        )
        user.set_password('12345678')
        db.session.add(user)
        db.session.commit()

        # 2. Создаем корзину для этого пользователя
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        
        # 3. Логинимся через виртуальный браузер
        client.post('/login', data={
            'nickname':'test_buyer',
            'new_password': '12345678'
        }, follow_redirects=True)

        # 4. Возвращаем клиент, который "запомнил" сессию пользователя
        return client



