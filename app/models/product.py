from app import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    discount = db.Column(db.Integer(), default=0)

    # db.ForeignKey - создает связь на стороне 'Много'
    # user_id = db.Column(db.Integer(), db.ForeignKey('users.id')) 
    
    photos = db.relationship('Photo', backref='product', lazy='dynamic')
    characteristics = db.relationship('Characteristic', backref='product', lazy='dynamic')
    product_in_carts = db.relationship('ProductInCart', backref='product', lazy='dynamic')

class Characteristic(db.Model):
    __tablename__ = 'characteristics'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    int_value = db.Column(db.Integer(), nullable=False)
    str_value = db.Column(db.String(30), nullable=False)
    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
    

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)

    photo_path = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
