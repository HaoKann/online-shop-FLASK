from app import create_app, db
from app.models import Product, Category, User  # Импортируем ваши модели
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("⏳ [1/3] Очистка базы данных...")
    db.drop_all()
    db.session.execute(text("DROP TABLE IF EXISTS alembic_version"))
    db.session.commit()
    print("✅ Старые данные удалены.")

    print("⏳ [2/3] Создание таблиц...")
    db.create_all()
    print("✅ Таблицы созданы.")

    print("⏳ [3/3] Добавление товаров (Seeding)...")
    
    try:
        # 1. Создаем Категории (без них товары не создать)
        cat_laptops = Category(name="Ноутбуки", slug="laptops")
        cat_phones = Category(name="Смартфоны", slug="smartphones")
        
        db.session.add_all([cat_laptops, cat_phones])
        db.session.commit() # Сохраняем, чтобы получить ID категорий

        # 2. Создаем Товары
        products = [
            Product(
                name="Игровой ноутбук Razor",
                price=1500,
                discount=10,
                category_id=cat_laptops.id,
                description="Мощный ноутбук для игр",
                image="laptop.jpg", # Убедитесь, что логика картинок позволяет строки
                is_active=True,
                stock=10
            ),
            Product(
                name="iPhone 15 Pro",
                price=1200,
                discount=0,
                category_id=cat_phones.id,
                description="Новейший смартфон",
                image="phone.jpg",
                is_active=True,
                stock=50
            ),
            Product(
                name="MacBook Air M2",
                price=1100,
                discount=5,
                category_id=cat_laptops.id,
                description="Легкий и быстрый",
                image="macbook.jpg",
                is_active=True,
                stock=15
            )
        ]

        db.session.add_all(products)
        db.session.commit()
        print(f"✅ Успешно добавлено {len(products)} товаров!")
        
    except Exception as e:
        print(f"⚠️ Ошибка при добавлении данных: {e}")
        # Если ошибка в полях, раскомментируйте строку ниже, чтобы увидеть детали в логах:
        # raise e

    print("🚀 Готово! Сервер может запускаться.")