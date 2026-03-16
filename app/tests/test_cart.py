from app.models.product import Product, Category
from app.models.cart import ProductInCart
from app.models.user import User
from app import db

def test_add_product_to_cart(auth_client, app):
    """Тест: Авторизованный юзер может добавить товар в корзину."""

    # 1. ПОДГОТОВКА: Создаем категорию и товар
    with app.app_context():
        category = Category(name='Процессоры', slug='cpu')
        db.session.add(category)
        db.session.commit()

        product = Product(
            name='Intel Core i9 Test',
            price=300000,
            discount=0,
            is_active=True,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()

        # Запоминаем ID созданного товара
        product_id = product.id

    # 2. ДЕЙСТВИЕ: Авторизованный клиент жмет кнопку "Добавить в корзину"
    # Отправляем POST-запрос на маршрут добавления товара
    # ВАЖНО: Мы используем auth_client, а не обычный client!
    response = auth_client.post(f'/cart/add_product/{product_id}')

    # 3. ПРОВЕРКИ
    # Сервер должен перенаправить нас обратно (код 302) после добавления
    assert response.status_code == 302

    # Проверяем базу данных: появился ли товар в корзине?
    with app.app_context():
        # Находим нашего тестового юзера (по никнейму из conftest.py)
        user = User.query.filter_by(nickname='test_buyer').first()

        # Ищем запись в ProductInCart для корзины этого юзера и нашего товара
        item_in_cart = ProductInCart.query.filter_by(
            cart_id=user.cart.id,
            product_id=product_id
        ).first()
        
        # Товар должен существовать в БД корзины и его количество должно быть = 1
        assert item_in_cart is not None
        assert item_in_cart.amount == 1