from app.models.product import Product, Category, ReadyPC, ProductInReadyPC
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


def test_add_ready_pc_to_cart(auth_client, app):
    """Тест: Проверяем добавление всех товаров из готовой сборки в корзину."""

    with app.app_context():
        # 1. ПОДГОТОВКА: Создаем компоненты и сборку
        category = Category(name='Видеокарты', slug='gpu')
        db.session.add(category)
        db.session.commit()

        # Создаем два товара для нашей сборки
        gpu = Product(name='RTX 4090', price=200000, discount=0, is_active=True, category_id=category.id)
        cpu = Product(name='Intel Core I9', price=100000, discount=0, is_active=True, category_id=category.id)
        db.session.add_all([gpu,cpu])
        db.session.commit()

        # Создаем саму готовую сборку
        ready_pc = ReadyPC(name='Super Gamer PC', category='Игровая', price=300000, amount=1, )
        db.session.add(ready_pc)
        db.session.commit()

        # Связываем товары со сборкой через промежуточную таблицу ProductInReadyPC
        link1 = ProductInReadyPC(ready_pc_id=ready_pc.id, product_id=gpu.id)
        link2 = ProductInReadyPC(ready_pc_id=ready_pc.id, product_id=cpu.id)
        db.session.add_all([link1, link2])
        db.session.commit()

        # Запоминаем ID сборки
        pc_id = ready_pc.id
    
    # 2. ДЕЙСТВИЕ: Отправляем запрос на добавление сборки
    response = auth_client.post(f'/cart/add_ready_pc/{pc_id}')

    # 3. ПРОВЕРКИ
    assert response.status_code == 302 # Должен быть редирект

    with app.app_context():
        user = User.query.filter_by(nickname='test_buyer').first()

        # Запрашиваем все товары в корзине этого пользователя
        products_in_cart = ProductInCart.query.filter_by(cart_id=user.cart.id).all()

        # Корзина должна содержать ровно 2 товара (GPU и CPU)
        assert len(products_in_cart) == 2

        # Вытаскиваем названия товаров из корзины
        product_names_in_cart = [item.product.name for item in products_in_cart]

        # Проверяем, что нужные товары действительно добавились
        assert 'RTX 4090' in product_names_in_cart
        assert 'Intel Core I9' in product_names_in_cart

def test_increase_amount(auth_client, app):
    """Тест: Увеличение количества товара в корзине (AJAX/JSON)."""

    with app.app_context():
        category = Category(name='Оперативная память', slug='ram')
        db.session.add(category)
        db.session.commit()

        product = Product(name='16GB DDR4', price=5000, category_id=category.id, is_active=True)
        db.session.add(product)
        db.session.commit()

        user = User.query.filter_by(nickname='test_buyer').first()
        cart_item = ProductInCart(amount=1, product_id=product.id, cart_id=user.cart.id)
        db.session.add(cart_item)
        db.session.commit()

        item_id = cart_item.id

    # Действие: Отправляем POST-запрос на увеличение
    response = auth_client.post(f'/cart/increase_amount/{item_id}')

    # Проверка: Сервер должен ответить статусом 200 и вернуть JSON
    assert response.status_code == 200

    # response.json автоматически превращает JSON-ответ сервера в словарь Python
    data = response.json
    assert data['status'] == 'success'
    assert data['new_quantity'] == 2
    assert data['item_total'] == 10000


def test_decrease_amount(auth_client, app): 
    """Тест: Уменьшение количества товара в корзине (AJAX/JSON)."""

    with app.app_context():
        category = Category(name='Кулеры', slug='cooler')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Deepcool', price=2000, category_id=category.id, is_active=True)
        db.session.add(product)
        db.session.commit()

        user = User.query.filter_by(nickname='test_buyer').first()
        cart_item = ProductInCart(amount=2, product_id=product.id, cart_id=user.cart.id)
        db.session.add(cart_item)
        db.session.commit()

        item_id = cart_item.id

    # Действие: Уменьшаем количество
    response = auth_client.post(f'/cart/decrease_amount/{item_id}')

   # Проверка: JSON ответ должен показать количество 1
    assert response.status_code == 200
    # response.json автоматически превращает JSON-ответ сервера в словарь Python
    data = response.json
    assert data['status'] == 'success'
    assert data['new_quantity'] == 1


def test_delete_product_from_cart(auth_client, app): 
    """Тест: Удаление товара из корзины (AJAX/JSON)."""

    with app.app_context():
        category = Category(name='Мышки', slug='mice')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Razer', price=4000, category_id=category.id, is_active=True)
        db.session.add(product)
        db.session.commit()

        user = User.query.filter_by(nickname='test_buyer').first()
        cart_item = ProductInCart(amount=1, product_id=product.id, cart_id=user.cart.id)
        db.session.add(cart_item)
        db.session.commit()

        item_id = cart_item.id

    # Действие: Удаляем товар (POST запрос, как у тебя в контроллере)
    response = auth_client.post(f'/cart/delete_product/{item_id}')

    assert response.status_code == 200
    # response.json автоматически превращает JSON-ответ сервера в словарь Python
    data = response.json
    assert data['status'] == 'success'

    # Проверяем БД: товар должен исчезнуть
    with app.app_context():
        deleted_item = db.session.get(ProductInCart, item_id)
        assert deleted_item is None
    
    








