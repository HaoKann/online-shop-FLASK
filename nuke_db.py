from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("⏳ Начинаем полную пересборку базы данных...")
    
    # 1. Удаляем всё старое
    try:
        db.drop_all()
        print("✅ Старые таблицы удалены.")
    except Exception as e:
        print(f"⚠️ Ошибка при удалении (не критично): {e}")

    # 2. Чистим хвосты миграций
    try:
        db.session.execute(text("DROP TABLE IF EXISTS alembic_version"))
        db.session.commit()
        print("✅ История миграций очищена.")
    except Exception as e:
        print(f"⚠️ Ошибка при очистке истории: {e}")

    # 3. САМОЕ ГЛАВНОЕ: Создаем таблицы напрямую
    try:
        db.create_all()
        print("🚀 Таблицы успешно созданы через db.create_all()!")
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА при создании таблиц: {e}")