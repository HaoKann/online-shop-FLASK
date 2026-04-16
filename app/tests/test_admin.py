from app.models.user import User
from app.models.product import Category, Product, Review, Characteristic, ReadyPC, Photo, ProductInReadyPC, CategoryCharacteristic
from app.models.order import Order
from app.models.faq import FAQ
from app import db
import io


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


def test_admin_faq_management_cycle(auth_client, app):
    """Комплексный тест: Создание, редактирование и удаление FAQ администратором."""

    # 1. ПОДГОТОВКА: Делаем юзера админом
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True
        db.session.commit()

    # 2. ДОБАВЛЕНИЕ: Создаем новый вопрос
    response_add = auth_client.post('/admin/admin/faqs/add', data={
        'question': 'Как проверить статус сборки?',
        'answer': 'В личном кабинете в разделе Заказы',
        'category': 'Общие вопросы'
    }, follow_redirects=True)

    assert response_add.status_code == 200
    assert 'Новый вопрос успешно добавлен!' in response_add.data.decode('utf-8')

    with app.app_context():
        faq = FAQ.query.filter_by(question='Как проверить статус сборки?').first()
        assert faq is not None
        assert faq.answer == 'В личном кабинете в разделе Заказы'
        faq_id = faq.id

    # 3. РЕДАКТИРОВАНИЕ: Изменяем созданный вопрос
    response_edit = auth_client.post(f'/admin/admin/faqs/edit/{faq_id}', data={
        'question': 'Как проверить статус?',
        'answer': 'Изменено: через бота или сайт',
        'category': 'Доставка'
    }, follow_redirects=True)

    assert response_edit.status_code == 200
    assert 'Вопрос успешно обновлен!' in response_edit.data.decode('utf-8')

    with app.app_context():
        updated_faq = db.session.get(FAQ, faq_id)
        assert updated_faq.question == 'Как проверить статус?'
        assert updated_faq.category == 'Доставка'


    # 4. СПИСОК: Проверяем отображение в общем списке
    response_list = auth_client.get('/admin/admin/faqs')
    assert response_list.status_code == 200
    assert 'Как проверить статус?' in response_list.data.decode('utf-8')


    # 5. УДАЛЕНИЕ: Проверяем удаление вопроса
    response_delete = auth_client.post(f'/admin/admin/faqs/delete/{faq_id}', follow_redirects=True)
    assert response_delete.status_code == 200
    assert 'Вопрос удален' in response_delete.data.decode('utf-8')

    with app.app_context():
        delete_faq = db.session.get(FAQ, faq_id)
        assert delete_faq is None


def test_admin_add_and_delete_characteristic(auth_client, app):
    """Тест: Добавление и удаление характеристики у конкретного товара."""
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        cat = Category(name='Комплектующие', slug='components')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='Процессор', price=10000, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()
        prod_id = prod.id

    # 1. ДОБАВЛЕНИЕ ХАРАКТЕРИСТИКИ
    # Имитируем отправку формы characteristics_form (важно передать submit_characteristics)
    response_add = auth_client.post(f'/admin/admin/products/{prod_id}', data={
        'characteristics_form-name': 'Сокет',
        'characteristics_form-value': 'AM4',
        'characteristics_form-value_type': 'string',
        'characteristics_form-submit_characteristics': 'Добавить'
    }, follow_redirects=True)

    assert response_add.status_code == 200

    with app.app_context():
        char = Characteristic.query.filter_by(prod_id=prod_id, name='Сокет').first()
        assert char is not None
        char_id = char.id

    # 2. УДАЛЕНИЕ ХАРАКТЕРИСТИКИ
    response_delete = auth_client.post(f'/admin/characteristic/delete/{char_id}', follow_redirects=True)
    assert response_delete.status_code == 200

    with app.app_context():
        assert db.session.get(Characteristic, char_id) is None


def test_admin_add_and_delete_readypc(auth_client, app):
    """Тест: Создание и удаление Готовой Сборки ПК."""
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True
        db.session.commit()

    # 1. ДОБАВЛЕНИЕ СБОРКИ
    response_add = auth_client.post('/admin/admin/add/ready-pc', data={
        'name': 'Игровой ПК',
        'category': 'gaming',
        'price': '500000'
    }, follow_redirects=True)

    assert response_add.status_code == 200
    assert 'Готовая сборка создана!' in response_add.data.decode('utf-8')

    with app.app_context():
        ready_pc = ReadyPC.query.filter_by(name='Игровой ПК').first()
        assert ready_pc is not None
        pc_id = ready_pc.id

    # 2. УДАЛЕНИЕ СБОРКИ
    response_delete = auth_client.post(f'/admin/admin/ready-pc/delete/{pc_id}', follow_redirects=True)
    assert response_delete.status_code == 200

    with app.app_context():
        assert db.session.get(ReadyPC, pc_id) is None


def test_admin_add_and_delete_photo(auth_client, app):
    """Тест: Имитация загрузки и удаления фотографии товара администратором."""
    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True
        db.session.commit()

        cat = Category(name='ФотоТест', slug='photo_test')
        db.session.add(cat)
        db.session.commit()

        prod = Product(name='Товар для фото', price=100, category_id=cat.id)
        db.session.add(prod)
        db.session.commit()
        prod_id = prod.id
    
    # 1. ЗАГРУЗКА ФОТО
    # Создаем фейковый файл в памяти
    fake_file = (io.BytesIO(b"fake image data"), 'test_image.jpg')

    # Отправляем форму (важно указать content_type='multipart/form-data' для файлов)
    response_add = auth_client.post(
        f'/admin/admin/products/{prod_id}/add_photo',
        data={'photo': fake_file},
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert response_add.status_code == 200
    assert 'Фото успешно добавлено!' in response_add.data.decode('utf-8')

    with app.app_context():
        photo = Photo.query.filter_by(prod_id=prod_id).first()
        assert photo is not None
        photo_id = photo.id

    # 2. УДАЛЕНИЕ ФОТО
    response_del = auth_client.post(f'/admin/admin/photo/delete/{photo_id}', follow_redirects=True)
    assert response_del.status_code == 200

    with app.app_context():
        assert db.session.get(Photo, photo_id) is None


def test_admin_edit_readypc(auth_client, app):
    """Тест: Редактирование состава готовой сборки ПК."""
    # 1. Отключаем CSRF только для этого теста, чтобы форма точно "пролезла"
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        # 1. Создаем ВСЕ необходимые категории комплектующих
        slugs = ['cpu', 'gpu', 'motherboard', 'ram', 'psu', 'cooler', 'storage', 'pc_case']
        cat_map = {}
        for s in slugs:
            c = Category(name=s.upper(), slug=s)
            db.session.add(c)
            db.session.flush() # Получаем ID не прерывая транзакцию
            cat_map[s] = c.id

        # 2. Создаем по одному товару для каждой категории
        product_ids = {}
        for s in slugs:
            p = Product(name=f'Test {s}', price=1000, category_id=cat_map[s], is_active=True)
            db.session.add(p)
            db.session.flush()
            product_ids[s] = str(p.id)

        rpc = ReadyPC(name='Старая сборка', price=50000, category='gaming')
        db.session.add(rpc)
        db.session.commit()
        
        rpc_id = rpc.id
        
    # 3. Отправляем ПОЛНЫЙ набор данных (все поля SelectField)
    form_data = {
        'name': 'Обновленная сборка',
        'price': 60000,
        'category': 'gaming'
    }
    form_data.update(product_ids) # Добавляем cpu, gpu, ram и т.д.

    response = auth_client.post(f'/admin/admin/ready-pc/edit/{rpc_id}', data=form_data, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        # Делаем refresh, чтобы SQLAlchemy точно подтянула новые данные из БД
        db.session.expire_all()
        updated_pc = db.session.get(ReadyPC, rpc_id)
        assert updated_pc.name == 'Обновленная сборка'

        # Проверяем, что хотя бы процессор привязался
        component = ProductInReadyPC.query.filter_by(ready_pc_id=rpc_id).first()
        assert component is not None


def test_admin_create_category_with_template(auth_client, app):
    """Тест: Создание категории с шаблоном характеристик."""

    # Отключаем проверку CSRF для этого теста
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        admin_user = User.query.filter_by(nickname='test_buyer').first()
        admin_user.is_admin = True

        cat = Category(name='Мониторы', slug='monitors')
        db.session.add(cat)
        db.session.commit()

        cat_id = cat.id

    # Отправляем POST запрос на добавление характеристики в шаблон
    response = auth_client.post(f'/admin/admin/categories/{cat_id}', data={
        'name': 'Герцовка',
        'value_type': 'string',
        'submit': 'Добавить'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        template = CategoryCharacteristic.query.filter_by(category_id=cat_id, name='Герцовка').first()
        assert template is not None
        assert template.value_type == 'string'