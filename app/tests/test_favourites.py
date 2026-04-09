from app.models.product import Product, Category
from app.models.user import User
from app import db

def test_favoutires_cycle(auth_client, app):
    """Тест: Добавление в избранное, просмотр и удаление."""
    with app.app_context():
        cat = Category(name='Перифирия', slug='perip')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='Клавиатура', price=3000, category_id=cat.id, is_active=True)
        db.session.add(prod)
        db.session.commit()
        prod_id = prod.id

    # 1. Добавляем в избранное
    response_add = auth_client.post(f'/favourites/add_product/{prod_id}', follow_redirects=True)
    assert response_add.status_code == 200

    # 2. Проверяем страницу избранного
    response_list = auth_client.get('/favourites')
    assert response_list.status_code == 200
    assert 'Клавиатура' in response_list.data.decode('utf-8')

    # 3. Удаляем из избранного
    response_del = auth_client.post(f'/favourites/delete_product/{prod_id}', follow_redirects=True)
    assert response_del.status_code == 200

    response_list_empty = auth_client.get('/favourites')
    assert 'Клавиатура' not in response_list_empty.data.decode('utf-8')
