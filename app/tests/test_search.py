from app.models.product import Product, Category
from app import db

def test_search_functional(client, app): 
    """Тест: Поиск товаров по названию."""
    with app.app_context():
        cat = Category(name='Компьютеры', slug='pcs')
        db.session.add(cat)
        db.session.commit()

        # Создаем товары с уникальными именами
        p1 = Product(name='Игровой ПК', price=1000000, category_id=cat.id, is_active=True)
        p2 = Product(name='Офисный ноутбук', price=300000, category_id=cat.id, is_active=True)
        p3 = Product(name='Скрытый товар', price=100, category_id=cat.id, is_active=False) 
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        # Сценарий 1: Ищем слово "Игровой"
        response = client.get('/search?q=Игровой')
        assert response.status_code == 200
        assert 'Игровой' in response.data.decode('utf-8')
        assert 'Офисныый' not in response.data.decode('utf-8')

        # Сценарий 2: Ищем то, чего нет
        response_empty = client.get('/search?q=кофеварка')
        assert response_empty.status_code == 200
        html_content = response_empty.data.decode('utf-8').lower()

        assert 'ничего' in html_content
        

        # Сценарий 3: Поиск не должен находить неактивные товары
        response_hidden = client.get('/search?q=Скрытый')
        assert 'Скрытый товар' not in response_hidden.data.decode('utf-8')
