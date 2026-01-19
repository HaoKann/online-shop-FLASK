from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Полностью уничтожаем старую структуру в облаке
    db.drop_all()
    # Удаляем таблицу версий, если она осталась
    db.session.execute(text("DROP TABLE IF EXISTS alembic_version"))
    db.session.commit()
    print("☢️ Облачная база уничтожена и готова к новой жизни!")