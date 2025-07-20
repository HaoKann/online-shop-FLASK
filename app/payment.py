import stripe
from flask import jsonify, request
from app import app
from flask_login import login_required, current_user

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment():
    try:
        # Получаем итоговую сумму из корзины (в копейках/тиинах)
        amount_in_cents = current_user.cart.sum_of_products_in_cart() * 100

        # Создаем "намерение платежа"
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency='kzt',
        )
        # Отправляем секретный ключ клиенту
        return jsonify({'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403