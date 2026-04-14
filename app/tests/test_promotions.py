from app.models.product import Product, Category
from app import db

def test_promotions_page(client, app):
    """Тест: Страница акций отображает товары со скидкой."""
    with app.app_context():
        cat = Category(name='Скидки', slug='sales')
        db.session.add(cat)
        db.session.commit()

        # Делаем скидочный товар
        p_sale = Product(name='Товар со скидкой', price=1000, discount=20, category_id=cat.id, is_active=True)
        # Делаем обычный товар
        p_default = Product(name='Обычный товар', price=1000, discount=0, category_id=cat.id, is_active=True)

        db.session.add_all([p_sale, p_default])
        db.session.commit()

    response = client.get('/promotions')
    assert response.status_code == 200
    html = response.data.decode('utf-8')

    assert 'Товар со скидкой' in html
