from app import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)

    # --- Содержание отзыва ---
    rating = db.Column(db.Integer, nullable=False) # Оценка от 1 до 5
    text = db.Column(db.Text, nullable=False)   # Текст отзыва
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Модерация и статус ---
    is_approved = db.Column(db.Boolean, default=False) # True, если отзыв одобрен админом

    # --- Связи (Внешние ключи) ---
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    ready_pc_id = db.Column(db.Integer, db.ForeignKey('readypc.id'), nullable=True)

    # --- Отношения (Relationship) ---
    # Позволяет получить объект User и Product, связанных с этим отзывом
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f'<Review {self.id} | Rating {self.rating}>'

