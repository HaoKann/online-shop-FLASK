from app.models.user import User
from app.models.product import Category, Product
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

        # Добавим немного базовых данных, чтобы списки в админке не были пустыми и код отработал
        cat = Category(name='Тест', slug='test')
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