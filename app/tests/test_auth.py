from app.models.user import User
from datetime import date
from app import db

def test_login_success(client, app):
    """Тест: Проверяем, что пользователь может успешно войти на сайт."""

    # 1. ПОДГОТОВКА: Создаем пользователя в тестовой базе
    user = User(
        name='Тестовый Ниндзя', 
        nickname='test_ninja', 
        email='ninja@example.com', 
        date_of_birth=date(2000, 1, 1))
    user.set_password('12345678')
    db.session.add(user)
    db.session.commit()

    # 2. ДЕЙСТВИЕ: Отправляем данные формы на сервер (POST-запрос)
    response = client.post('/login', data={
        'nickname': 'ninja@example.com',
        'new_password': '12345678'
    }, follow_redirects=False) 
    # follow_redirects=True означает: "если сервер скажет перенаправить на главную страницу после входа - переходи"

    # 3. ПРОВЕРКА:
    # Если вход успешен, Flask вернет код 302 (Redirect) на главную или в профиль!
    assert response.status_code == 302


def test_login_failure(client, app):
    """Тест: Проверяем, что с неправильным паролем войти нельзя."""

    # 1. Создаем пользователя
    user = User(
        name='Плохой Хакер',
        nickname="hacker", 
        email="hacker@example.com",
        date_of_birth=date(1995, 5, 5))
    user.set_password('correct_password')
    db.session.add(user)
    db.session.commit()

    # 2. Пытаемся войти с НЕПРАВИЛЬНЫМ паролем
    response = client.post('/login', data={
        'nickname': 'hacker@example.com',
        'new_password': 'wrong_password_123'
    }, follow_redirects=True)

    # 3. Проверяем, что нас НЕ пустило (имя hacker не должно появиться как у авторизованного)
    # И мы всё еще видим кнопку или текст, связанный с ошибкой входа
    assert response.status_code == 200
    assert b'hacker' not in response.data
