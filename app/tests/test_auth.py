from app.models.user import User
from app import db

def test_login_success(client, app):
    """Тест: Проверяем, что пользователь может успешно войти на сайт."""

    # 1. ПОДГОТОВКА: Создаем пользователя в тестовой базе
    user = User(nickname='test_ninja', email='ninja@example.com')
    user.set_password('12345678')
    db.session.add(user)
    db.session.commit()

    # 2. ДЕЙСТВИЕ: Отправляем данные формы на сервер (POST-запрос)
    response = client.post('/login', data={
        'email': 'ninja@example.com',
        'password': '12345678'
    }, follow_redirects=True) 
    # follow_redirects=True означает: "если сервер скажет перенаправить на главную страницу после входа - переходи"

    # 3. ПРОВЕРКИ:
    assert response.status_code == 200
    assert b'test_ninja' in response.data

