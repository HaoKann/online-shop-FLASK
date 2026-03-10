import pytest
from app import create_app, db
from app.config import Config

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

@pytest.fixture
def client(app):
    """Создаем виртуальный браузер (test_client) для симуляции действий пользователя."""
    return app.test_client()

