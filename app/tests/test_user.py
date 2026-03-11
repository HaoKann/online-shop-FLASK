from app.models.user import User

def test_user_password_hashing(app):
    """Тест 1: Проверяем, что пароли шифруются и проверяются корректно."""

    # 1. Подготовка: создаем пользователя (в базу пока можно даже не сохранять)
    user = User(nickname='test_ninja', email='ninja@example.com')

    # Задаем пароль
    user.set_password('12345678')

    # 2. Проверка безопасности:
    # Убеждаемся, что пароль НЕ сохранился в открытом виде
    assert user.password_hash != '12345678'

    # Убеждаемся, что правильный пароль проходит проверку
    assert user.check_password('12345678') is True

    # Убеждаемся, что неправильный пароль отвергается
    assert user.check_password('wrong_password') is False