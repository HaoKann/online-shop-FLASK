def test_hompage_loads(client):
    """Проверяем, что главная страница сайта открывается и отдает статус 200 (OK)."""

    # Наш виртуальный браузер заходит на главную страницу
    response = client.get('/')

    # Проверяем, что сервер ответил "Всё хорошо" (код 200)
    assert response.status_code == 200

    # Проверяем, что на странице есть наше название (например, "PerfectPC" или "Почему выбирают нас")
    assert b"PerfectPC" in response.data or b"Perfect PC" in response.data
