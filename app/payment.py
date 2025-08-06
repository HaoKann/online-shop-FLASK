# Задача: Безопасно сообщить Stripe о том, что клиент собирается совершить платеж, 
# и получить от Stripe одноразовое "разрешение" на эту операцию.

# 1.Расчет суммы: Когда пользователь заходит на страницу оплаты,  JavaScript первым делом отправляет запрос на этот маршрут. 
# Код на сервере берет сумму из корзины и обязательно переводит ее в тиыны (* 100), 
# так как Stripe всегда работает в минимальных единицах валюты, чтобы избежать ошибок с дробями.

# 2. Создание PaymentIntent: Это ключевой момент. Сервер обращается к Stripe и говорит, 
# что необходимо подготовится к операции проведения оплаты на сумму из корзины.
# Stripe создает у себя запись об этом "намерении" и присваивает ему уникальный ID

# 3. Возврат client_secret: В ответ Stripe возвращает серверу специальный, одноразовый ключ — client_secret. 
# Этот ключ является разрешением для сайта 1 раз провести операцию именно на эту сумму. 
# Сервер немедленно отправляет этот client_secret обратно в браузер клиента.

# Итог бэкенда: Сервер никогда не видел данные карты. 
# Он просто выступил посредником, который договорился со Stripe о сумме и получил разрешение на оплату.

import stripe
from flask import jsonify, current_app, Blueprint
from flask_login import login_required, current_user

# Создаем Blueprint
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    
    try:
        cart_total = current_user.cart.sum_of_products_in_cart()

        # Проверяем, что корзина не пуста
        if not cart_total or cart_total <= 0:
            return jsonify(error='Сумма для оплаты некорректна или корзина пуста'), 400

        # --- УПРОЩЕНИЕ 1: Работаем напрямую с тенге ---
        # Stripe требует сумму в минимальных единицах (тиынах), поэтому умножаем на 100
        amount_in_tiyn = int(cart_total * 100)

        # Минимальная сумма для платежа в Stripe ~200-250 KZT
        if amount_in_tiyn < 25000: # 250 KZT в тиынах
            return jsonify({'error': 'Минимальная сумма для оплаты 250 ₸'}), 400

        # Создаем PaymentIntent в тенге
        intent = stripe.PaymentIntent.create(
            amount=amount_in_tiyn,
            currency='kzt',
            description=f'Оплата заказа от {current_user.email}'
        )

        return jsonify({'clientSecret': intent.client_secret})
    
    # --- УПРОЩЕНИЕ 2: Объединяем обработку ошибок ---
    # Ловим все возможные ошибки от Stripe в одном блоке
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
        return jsonify(error=str(e)), 400
    # Ловим все остальные ошибки (например, если нет корзины у пользователя)
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify(error="Внутренняя ошибка сервера"), 500