from app import db, login_manager
from datetime import datetime,timezone 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    date_of_birth = db.Column(db.DateTime(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    update_date = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    avatar = db.Column(db.String(256))

    # db.relationship - описывает связь на стороне 'Один'
    # Если нужно из User('1') обратиться к Product('Много') то использую products
    # Если нужно из Product обратиться к User то использую backref - user
    # products = db.relationship('Product', backref='user', lazy='dynamic')

    cart = db.relationship('Cart', backref='user', uselist=False)
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_avatar(self):
        return 'avatars/' + str(self.id) + '/' + self.avatar