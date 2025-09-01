from app import db

class FAQ(db.Model):
    __tablename__ = 'faqs' 

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    # Поле для группировки вопросов, например: "Доставка", "Оплата"
    category = db.Column(db.String(100), nullable=False, index=True)

    def __repr__(self):
        return f'FAQ {self.question}'