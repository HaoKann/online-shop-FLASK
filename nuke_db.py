from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Импортируем классы напрямую из их файлов внутри папки models
    try:
        from app.models.product import Product
        from app.models.product import Category # Если Category в файле product.py
    except ImportError:
        # Если Category в отдельном файле (проверь, есть ли category.py в списке ls)
        try:
            from app.models import Category
        except:
            # Если нет файла category.py, возможно она в product.py или другом
            print("⚠️ Не удалось найти модель Category. Проверь имя файла!")
            Category = None

    print("⏳ [1/2] Очистка и создание таблиц...")
    db.drop_all()
    db.create_all()
    print("✅ Таблицы созданы.")

    if Product and Category:
        print("⏳ [2/2] Добавление тестовых данных...")
        try:
            # Создаем категории
            # ВНИМАНИЕ: Проверь, есть ли поле 'slug' в твоей модели Category
            c1 = Category(name="Ноутбуки", slug="laptops")
            c2 = Category(name="Смартфоны", slug="smartphones")
            db.session.add_all([c1, c2])
            db.session.commit()

            # Создаем товары
            p1 = Product(
                name="Игровой ноутбук Razor",
                price=1500,
                category_id=c1.id,
                is_active=True
            )
            p2 = Product(
                name="iPhone 15 Pro",
                price=1200,
                category_id=c2.id,
                is_active=True
            )
            
            db.session.add_all([p1, p2])
            db.session.commit()
            print(f"✅ Успешно добавлено {db.session.query(Product).count()} товаров!")
        except Exception as e:
            print(f"❌ Ошибка при заполнении: {e}")
            db.session.rollback()

    print("🚀 Готово! Проверяй сайт.")