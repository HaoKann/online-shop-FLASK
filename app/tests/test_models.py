from app.models.product import Product, Category
from app import db

# Передаем фикстуру 'app', чтобы тест выполнялся внутри настроенного 
# контекста (с нашей временной базой данных)
def test_product_no_discount(app):
    """Тест 1: Если скидки нет (0), финальная цена равна базовой."""

    # 1. Сначала создаем категорию (иначе БД не разрешит создать товар)
    category = Category(name='Периферия', slug='peripherals')
    db.session.add(category)
    db.session.commit() # Сохраняем, чтобы у категории появился ID

    # 2. Создаем товар и привязываем его к категории
    product = Product(
        name='Обычная мышка',
        price=10000,
        discount=0,
        is_active=True,
        category_id=category.id
    )
    db.session.add(product)
    db.session.commit()

    # 2. Действие (Act): достаем из БД
    saved_product = Product.query.filter_by(name='Обычная мышка').first()

    # 3. Проверка (Assert): математика должна сойтись
    assert saved_product is not None
    assert saved_product.get_discount_price() == 10000

def test_product_with_discount(app):
    """Тест 2: Если скидка 20%, финальная цена должна считаться верно."""
    # 1. Создаем категорию
    category = Category(name='Комплектующие', slug='components')
    db.session.add(category)
    db.session.commit()

    # 1. Подготовка: создаем акционный товар
    product = Product(
        name='Игровая клавиатура',
        price=20000,
        discount=20, # Скидка 20%
        is_active=True,
        category_id=category.id
    )
    db.session.add(product)
    db.session.commit()

    # 2. Действие
    saved_product = Product.query.filter_by(name='Игровая клавиатура').first()

    # 3. Проверка: 20000 - 20% = 16000
    assert saved_product.get_discount_price() == 16000