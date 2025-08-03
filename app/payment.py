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

# Создаем Blueprint (если вы еще не сделали этого)
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        print("--- DEBUG: Запрос вошел в функцию create_payment ---")
        
        cart_total = current_user.cart.sum_of_products_in_cart()
        print(f"--- DEBUG: Сумма из корзины: {cart_total} ---")

        if not cart_total or cart_total <= 0:
            print("--- DEBUG: ОШИБКА! Сумма некорректна. ---")
            return jsonify(error='Сумма для оплаты некорректна или корзина пуста'), 400

        # Конвертация суммы в центы для USD (пример, 1 тенге = 0.0023 USD, но лучше использовать реальный курс)
        amount_in_cents = int(cart_total * 0.0023 * 100)
        print(f"--- DEBUG: Сумма в центах (USD): {amount_in_cents} ---")

        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency='usd',
            description=f'Оплата заказа пользователя {current_user.id}'
        )
        print("--- DEBUG: PaymentIntent успешно создан! ---")
        return jsonify({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        print(f"--- DEBUG: КРИТИЧЕСКАЯ ОШИБКА Stripe: {e} ---")
        return jsonify(error=str(e)), 400
    except Exception as e:
        # ЭТОТ БЛОК ПОЙМАЕТ ТОЧНУЮ ОШИБКУ
        print(f"--- DEBUG: КРИТИЧЕСКАЯ ОШИБКА: {e} ---")
        return jsonify(error=str(e)), 400