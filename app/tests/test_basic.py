def test_hompage_loads(client):
    """Проверяем, что главная страница сайта открывается и отдает статус 200 (OK)."""

    # Наш виртуальный браузер заходит на главную страницу
    response = client.get('/')

    # Проверяем, что сервер ответил "Всё хорошо" (код 200)
    assert response.status_code == 200

    # Проверяем, что на странице есть наше название (например, "PerfectPC" или "Почему выбирают нас")
    assert b"PerfectPC" in response.data or b"Perfect PC" in response.data

def test_404_error_page(client):
    """Тест: Проверяем, что сайт правильно обрабатывает несуществующие адреса."""

    # Виртуальный браузер пытается зайти на несуществующую страницу 
    response = client.get('/page_does_not_exist')

    # Сервер должен честно признаться, что такой страницы нет (код 404)
    assert response.status_code == 404