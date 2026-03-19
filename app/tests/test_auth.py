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


def test_register_success(client, app):
    """Тест: Успешная регистрация нового пользователя."""

    # Отправляем POST-запрос с данными нового пользователя
    response = client.post('/reg', data={
        'name': 'New Buyer',
        'nickname': 'new_buyer',
        'email': 'new_buyer@mail.ru',
        'date_of_birth': '2000-01-01',
        'phone_number':'+79991234567',
        'new_password':'superpassword123',
        'check_password': 'superpassword123'
    }, follow_redirects=False)

    # При успешной регистрации нас должно перекинуть на логин или главную (код 302)
    assert response.status_code == 302

    # Проверка БД
    with app.app_context():
        new_user = User.query.filter_by(email='new_buyer@mail.ru').first()

        assert new_user is not None
        assert new_user.nickname == 'new_buyer'
        assert new_user.name == 'New Buyer'


def test_register_duplicate_email(client, app):
    """Тест: Нельзя зарегистрироваться с уже занятым email."""

    # 1. ПОДГОТОВКА: Создаем первого юзера
    with app.app_context():
        user = User(
            name='First',
            nickname='first_user',
            email='taken@mail.ru',
            date_of_birth=date(1995, 5, 5),
            phone_number='+78888888888'
        )
        user.set_password('12345678')
        db.session.add(user)
        db.session.commit()


        # 2. ДЕЙСТВИЕ: Пытаемся зарегать ВТОРОГО юзера на ТОТ ЖЕ email
        response = client.post('/reg', data={
            'name': 'Clone',
            'nickname': 'clone_user',
            'email': 'taken@mail.ru',
            'date_of_birth': '2000-01-01',
            'phone_number': '+70000000000',
            'new_password': 'password123',
            'check_password': 'password123'
        }, follow_redirects=False)

        # 3. ПРОВЕРКА: Сервер должен отклонить запрос и вернуть форму (код 200)
        assert response.status_code == 200

        # Убеждаемся, что в базе по-прежнему только 1 юзер с таким email
        with app.app_context():
            users_with_email = User.query.filter_by(email='taken@mail.ru').all()
            assert len(users_with_email) == 1


