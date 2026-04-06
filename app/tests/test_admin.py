from app.models.user import User
from app.models.product import Category, Product, Review
from app.models.order import Order
from app.models.faq import FAQ
from app import db

def test_admin_access_denied_for_regular_users(auth_client):
    """Тест: Обычный юзер получает 403 при попытке зайти в админку."""

    # У auth_client (test_buyer) поле is_admin = False по умолчанию
    response = auth_client.get('/admin/admin')

    # Сервер должен строго отказать (Forbidden)
    assert response.status_code == 403

def test_admin_dashboard_and_lists(auth_client, app):
    """Тест: Админ может просматривать все главные страницы панели."""

    # 1. ПОДГОТОВКА: Делаем нашего тестового покупателя АДМИНОМ! 
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True
        db.session.commit()

        # СНАЧАЛА сохраняем категорию, чтобы БД выдала ей ID
        cat = Category(name='Тест', slug='test')
        db.session.add(cat)
        db.session.commit()

        # ТЕПЕРЬ создаем товар с реальным cat.id и остальное
        prod = Product(name='Админский товар', price=100, is_active=True, category_id=cat.id)
        order = Order(user_id=admin_user.id, price=100, status='pending')
        faq = FAQ(question='Вопрос', answer='Ответ', category='general')

        db.session.add_all([cat, prod, order, faq])
        db.session.commit()


    # 2. ДЕЙСТВИЕ: Теперь мы админы! Идем проверять все списки.
    endpoints = [
        '/admin/admin',               
        '/admin/admin/products',     
        '/admin/admin/categories',    
        '/admin/admin/user-orders',   
        '/admin/admin/ready-pcs',    
        '/admin/admin/faqs',          
        '/admin/admin/reviews'
    ]

    # 3. ПРОВЕРКА: Ни одна из страниц не должна упасть (ожидаем везде статус 200)
    for url in endpoints:
        response = auth_client.get(url)
        assert response.status_code == 200, f'Админ не смог открыть страницу {url}'


def test_admin_deactivate_and_activate_product(auth_client, app):
    """Тест: Админ может скрывать (is_active=False) и возвращать товары."""

    with app.app_context():
        # Снова даем права
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        cat = Category(name='Test2', slug='test2')
        db.session.add(cat)
        db.session.commit()

        # Создаем товар
        prod = Product(name='Скрытый', price=5000, is_active=True, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()

        prod_id = prod.id

    # 1. Деактивируем (вызываем POST запрос, как если бы нажали Confirm в форме)  
    resp_deactivate = auth_client.post(f'/admin/admin/deactivate_product/{prod_id}')
    assert resp_deactivate.status_code == 302 # Редирект после успеха

    with app.app_context():
        assert db.session.get(Product, prod_id).is_active == False

    # 2. Активируем обратно
    resp_activate = auth_client.post(f'/admin/admin/activate_product/{prod_id}')
    assert resp_activate.status_code == 302

    with app.app_context():
        db.session.get(Product, prod_id).is_active == True

def test_admin_delete_product(auth_client, app):
    """Тест: Админ может полностью удалить товар из БД."""
    
    with app.app_context():

        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        cat = Category(name='Удаление', slug='del')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='На удаление', price=100, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()

        prod_id = prod.id

        # Имитируем подтверждение удаления (POST запрос на форму ConfirmForm)
        response = auth_client.post(f'/admin/admin/delete_product/{prod_id}', follow_redirects=True)
        assert response.status_code == 200

        with app.app_context():
            assert db.session.get(Product, prod_id) is None


def test_admin_edit_order_status(auth_client, app):
    """Тест: Админ может менять статус заказа (например, на 'completed')."""
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True
        order = Order(user_id=admin_user.id, price=1000, status='pending')
        db.session.add(order)
        db.session.commit()

        order_id = order.id

        # Отправляем форму редактирования заказа
        response = auth_client.post(f'/admin/admin/user-orders/edit/{order_id}', data={
            'phone_number': '+77777777777',
            'email': 'admin@test.com',
            'address': 'Тестовый адрес', 
            'way_of_delivery': 'Самовывоз',
            'time_of_arrival': '12:00-18:00',
            'status': 'delivered'
        }, follow_redirects=True)

        assert response.status_code == 200
        with app.app_context():
            updated_order = db.session.get(Order, order_id)
            assert updated_order.status == 'delivered'


def test_admin_approve_reviews(auth_client, app):
    """Тест: Модерация отзывов (перевод из неактивных в одобренные)."""
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        prod = Product(name='Товар для отзыва', price=100, category_id=1)
        db.session.add(prod)
        db.session.commit()

        review = Review(text='Норм', rating=5, user_id=admin_user.id, product_id=prod.id, is_approved=False)
        db.session.add(review)
        db.session.commit()

        review_id = review.id

    # Одобряем отзыв
    response = auth_client.post(f'/admin/admin/reviews/approve/{review_id}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        assert db.session.get(Review, review_id).is_approved == True