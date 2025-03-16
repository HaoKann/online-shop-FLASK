from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Integer())
    discount = db.Column(db.Integer(), default=0)

class Characteristic(db.Model):
    __tablename__ = 'characteristics'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    int_value = db.Column(db.Integer())
    str_value = db.Column(db.String(30))

    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)

    photo_path = db.Column(db.String(100))
    description = db.Column(db.String(100))

    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
