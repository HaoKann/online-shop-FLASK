from app.models.product import Product, Category
from app.models.cart import ProductInCart
from app.models.order import Order, Delivery, ProductInOrder
from app.models.user import User
from app import db

def test_checkout_and_order_success(auth_client, app):
    '''Тест: Оформление доставки и успешное создание заказа'''

    # 1 ПОДГОТОВКА: Создаем товар и кладем в корзину нашего тестового юзера
    with app.app_context():
        category = Category(name='Клавиатуры', slug='keyboards')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Logitech', price=10000, discount=0, category_id=category.id, is_active=True)
        db.session.add(product)
        db.session.commit()

        user = User.query.filter_by(nickname='test_buyer').first()
        cart_item = ProductInCart(amount=1, product_id=product.id, cart_id=user.cart.id)
        db.session.add(cart_item)
        db.session.commit()

        product_id = product.id

        # 2 ДЕЙСТВИЕ 1: Отправляю данные доставки на /checkout
        response_checkout = auth_client.post('/checkout', data={
            'address': 'ул. Абая',
            'way_of_delivery': 'Самовывоз',
            'time_of_arrival': '7:00-11:00'
        })
        
        # Сервер должен перенаправить на страницу оплаты
        assert response_checkout.status_code == 302

        # 3 ДЕЙСТВИЕ 2: Имитируем успешную оплату 
        response_success = auth_client.get('/order-success')
        assert response_success.status_code == 200

        # Получаем весь текст HTML-страницы
        html_text = response_success.data.decode('utf-8')

        assert "Произошла ошибка при сохранении заказа" not in html_text, f"СЕРВЕР УПАЛ И ОТКАТИЛ ЗАКАЗ: {html_text}"

        # 4 Проверки в БД
        with app.app_context():
            user = User.query.filter_by(nickname='test_buyer').first()

            # создался ли заказ
            order = Order.query.filter_by(user_id = user.id).first()
            assert order is not None 
            assert order.status == 'pending'
            assert order.price == 10000

            #  прикрепилась ли доставка
            delivery = Delivery.query.filter_by(order_id=order.id).first()
            assert delivery is not None
            assert delivery.address == 'ул. Абая'

            #  перенесся ли товар в заказ
            product_in_order = ProductInOrder.query.filter_by(order_id=order.id).first()
            assert product_in_order is not None
            assert product_in_order.product_id == product_id

            # очистилась ли корзина
            assert user.cart.products_in_cart.count() == 0


def test_cancel_order(auth_client, app):
    '''Тест: Пользователь может отменит заказ со статусом pending'''
    
    # 1 Создаем заказ со статусом pending
    with app.app_context():
        user = User.query.filter_by(nickname='test_buyer').first()
        order = Order(user_id=user.id, price=5000, status='pending')
        db.session.add(order)
        db.session.commit()

        order_id = order.id

    # 2 Отменяем заказ через post запрос
    response = auth_client.post(f'/cancel_order/{order_id}')
    assert response.status_code == 302 # Редирект обратно на список заказов

    # 3 Проверка изменения статуса на 'cancel'
    with app.app_context():
        canceled_order = db.session.get(Order, order_id)
        assert canceled_order.status == 'canceled'
