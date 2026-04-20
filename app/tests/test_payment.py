from unittest.mock import patch, MagicMock
import stripe

def test_payment_intent_success(auth_client):
    """Тест: Успешное создание намерения на платеж."""

    # 1. Подменяем метод корзины, чтобы он всегда возвращал 5000 тенге (без БД)
    with patch('app.models.cart.Cart.sum_of_products_in_cart', return_value=5000):

        # 2. Подменяем вызов stripe.PaymentIntent.create
        with patch('app.payment.stripe.PaymentIntent.create') as mock_stripe:

            # Настраиваем, что должна вернуть наша "поддельная" функция Stripe
            mock_intent = MagicMock()
            mock_intent.client_secret = 'pi_123_secret_456'
            mock_stripe.return_value = mock_intent

            # 3. Делаем POST-запрос от авторизованного пользователя
            response = auth_client.post('/create-payment-intent')

            # 4. Проверяем результат
            assert response.status_code == 200
            assert response.json['clientSecret'] == 'pi_123_secret_456'

            # Проверяем, что Stripe был вызван с правильной суммой в тиынах (5000 * 100)
            mock_stripe.assert_called_once()
            args, kwargs = mock_stripe.call_args
            assert kwargs['amount'] == 500000
            assert kwargs['currency'] == 'kzt'


def test_payment_intent_empty_cart(auth_client):
    """Тест: Ошибка при пустой корзине."""
    with patch('app.models.cart.Cart.sum_of_products_in_cart', return_value=0):
        response = auth_client.post('/create-payment-intent')

        assert response.status_code == 400
        assert 'корзина пуста' in response.json['error']

def test_payment_intent_min_amount(auth_client):
    """Тест: Ошибка при сумме меньше 250 тенге."""
    # Возвращаем 200 тенге
    with patch('app.models.cart.Cart.sum_of_products_in_cart', return_value=200):
        response = auth_client.post('/create-payment-intent')

        assert response.status_code == 400
        assert 'Минимальная сумма' in response.json['error']

def test_payment_intent_stripe_error(auth_client):
    """Тест: Обработка официальной ошибки от Stripe."""
    with patch('app.models.cart.Cart.sum_of_products_in_cart', return_value=5000):
        with patch('app.payment.stripe.PaymentIntent.create') as mock_stripe:
            
            # side_effect заставляет mock "выбросить" исключение
            mock_stripe.side_effect = stripe.error.StripeError('Ваша карта отклонена')

            response = auth_client.post('/create-payment-intent')

            assert response.status_code == 400
            assert 'Ваша карта отклонена' in response.json['error']

def test_payment_intent_server_error(auth_client):
    """Тест: Обработка неожиданной ошибки (Exception)."""
    with patch('app.models.cart.Cart.sum_of_products_in_cart', return_value=5000):
        with patch('app.payment.stripe.PaymentIntent.create') as mock_stripe:

            # Имитируем падение, например, обрыв соединения (обычный Exception)
            mock_stripe.side_effect = Exception('Интернет отключился')

            response = auth_client.post('/create-payment-intent')

            assert response.status_code == 500
            assert 'Внутренняя ошибка сервера' in response.json['error']





