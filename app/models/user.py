from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.DateTime(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100))
    phone_number = db.Column(db.Integer())
    password_hash = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    update_date = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    avatar = db.Column(db.String(256))