from app.models.product import Product, Category
from app import db

def test_catalog_page_shows_products(client, app):
    """Тест 2: Проверяем, что страница каталога открывается и отображает товары из БД."""

    # 1. Подготовка: Создаем категорию и тестовый товар в нашей временной базе
    category = Category(name='Видеокарты', slug='gpu')
    db.session.add(category)
    db.session.commit()

    product = Product(
        name='RTX 4090 Test Edition',
        price=1500000,
        discount=0,
        is_active=True,
        category_id=category.id
    )
    db.session.add(product)
    db.session.commit()

    # 2. Действие: Наш виртуальный браузер (client) переходит по адресу каталога
    response = client.get('/catalog')

    # 3. Проверки:
    assert response.status_code == 200

    assert b'RTX 4090 Test Edition' in response.data
