from app.models.product import Product, Category
from app.models.review import Review
from app import db

def test_catalog_sorting_and_paginarion(client, app):
    """Тест: Главная страница каталога, сортировка и пагинация."""

    with app.app_context():
        # СНАЧАЛА создаем категорию, чтобы БД не ругалась на NOT NULL
        cat = Category(name='Тест', slug='test')
        db.session.add(cat)
        db.session.commit()


        # Создаем пару товаров с разной ценой и привязываем к категории
        p1 = Product(name='Дешевый', price=1000, is_active=True, category_id=cat.id)
        p2 = Product(name='Дорогой', price=9000, is_active=True, category_id=cat.id)
        db.session.add_all([p1, p2])
        db.session.commit()

        # Проверяем базовый каталог 
        response = client.get('/catalog')
        assert response.status_code == 200

        # Проверяем сортировку от лешевых к дорогим
        response_asc = client.get('/catalog?sort=price_asc')
        assert response_asc.status_code == 200

        # Проверяем сортировку от дорогих к дешевым + пагинацию
        response_desc = client.get('/catalog?sort=price_desc&page=1')
        assert response_desc.status_code == 200

def test_all_category_routes(client, app):
    """Тест: Проверяем, что ВСЕ 8 страниц категорий открываются без ошибок."""

    # Список всех маршрутов (endpoints) из твоего контроллера
    category_routes = [
        '/gpu', '/cpu', '/motherboard', '/psu',
        '/ram', '/cooler', '/storage', '/pc_case'
    ]

    # Создаем все нужные категории в БД чтобы страницы не были пустыми 
    with app.app_context():
        slugs = ['gpu', 'cpu', 'mothernoard', 'psu', '/ram', '/cooler', '/storage', '/pc_case']
        for slug in slugs:
            cat = Category(name=slug.upper(), slug=slug)
            db.session.add(cat)
            db.session.commit()

            # Добавляем по 1 товару в каждую категорию
            prod = Product(name=f'Товар {slug}', price=5000, is_active=True, category_id=cat.id)
            db.session.add(prod)
        db.session.commit()

    # В цикле заходим на каждую страницу и проверяем статус 200 ОК
    for route in category_routes:
        response = client.get(route)
        assert response.status_code == 200, f'Ошибка на маршруте {route}'


def test_product_details_and_reviews(auth_client, app):
    """Тест: Просмотр карточки товара и логика отзывов."""

    with app.app_context():
        cat = Category(name='Мыши', slug='mice')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='Супер Мышь', price=3000, is_active=True, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()

        prod_id = prod.id

    # 1. Проверяем, что страница товара открывается
    response = auth_client.get(f'/product_details/{prod_id}')
    assert response.status_code == 200

    # 2. Оставляем первый отзыв
    response_review = auth_client.post(f'/product_details/{prod_id}', data={
        'rating': 5,
        'text': 'Хорошая мышка'
    }, follow_redirects=True)

    assert response_review.status_code == 200

    # Проверяем БД: отзыв должен сохраниться со статусом is_approved=False
    with app.app_context():
        review = Review.query.filter_by(product_id=prod_id).first()
        assert review is not None
        assert review.text == 'Хорошая мышка'
        assert review.is_approved == False

    # 3. Попытка оставить второй отзыв на тот же товар (дубликат)
    response_duplicate = auth_client.post(f'/product_details/{prod_id}', data={
        'rating': 1,
        'text': 'Плохая мышка'
    }, follow_redirects=True)

    assert response_duplicate.status_code == 200

    # Проверяем БД: второй отзыв НЕ должен был сохраниться
    with app.app_context():
        all_reviews = Review.query.filter_by(product_id=prod_id).all()
        assert len(all_reviews) == 1 # Как был 1 отзыв, так и остался


def test_review_requires_login(client, app):
    """Тест: Анонимный пользователь не может оставить отзыв."""

    with app.app_context():
        cat = Category(name='Тест', slug='test')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='Товар для теста', price=1000, is_active=True, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()

        prod_id = prod.id

    # Используем обычный client (НЕ auth_client), значит мы Гость
    response = client.post(f'/product_details/{prod_id}', data={
        'rating': 4,
        'text': 'Пустите меня оставить отзыв!'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/login' in response.location

