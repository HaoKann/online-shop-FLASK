import pytest
from app import app as create_app, db

@pytest.fixture
def app():
    """Настраиваем приложение специально для тестов."""
    # Создаем экземпляр приложения через фабрику
    flask_app = create_app()
    
    # 1. Включаем режим тестирования (Flask будет вести себя строже к ошибкам)
    flask_app.config['TESTING'] = True

    # 2. САМОЕ ГЛАВНОЕ: Переключаем базу данных на временную (в оперативной памяти)
    # Она создается мгновенно и бесследно исчезает после окончания тестов. 
    # Твои реальные товары и юзеры в Postgres не пострадают!
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # 3. Отключаем CSRF-защиту форм, чтобы не мучиться с токенами в тестах
    flask_app.config['WTF_CSRF_ENABLED'] = False

    # Создаем контекст приложения (чтобы Flask понимал, с чем работает)
    with flask_app.app_context():
        # Создаем все таблицы в нашей чистой временной базе
        db.create_all()

        # Передаем настроенное приложение тестам
        yield flask_app

        # ПОСЛЕ ТЕСТОВ: уничтожаем сессию и удаляем все таблицы (уборка за собой)
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Создаем виртуальный браузер (test_client) для симуляции действий пользователя."""
    return app.test_client()

