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
    
    photos = db.relationship('Photo', backref='product', lazy='dynamic', 
                           cascade='all, delete-orphan', passive_deletes=True)
    characteristics = db.relationship('Characteristic', backref='product', lazy='dynamic',
                                    cascade='all, delete-orphan', passive_deletes=True)
    product_in_carts = db.relationship('ProductInCart', backref='product', lazy='dynamic',
                                     cascade='all, delete-orphan', passive_deletes=True)
    favourite_by_users = db.relationship('FavouriteProduct', backref='product', lazy='dynamic',
                                       cascade='all, delete-orphan', passive_deletes=True)
    

    def get_first_photo(self):
        if self.photos.first():
            return self.photos.first().get_photo()
        else:
            return '/static/img/default.webp'

class Characteristic(db.Model):
    __tablename__ = 'characteristics'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    int_value = db.Column(db.Integer(), nullable=False)
    str_value = db.Column(db.String(30), nullable=False)
    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)

    photo_path = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    def get_photo(self):
        return  '/static/products_photo/' + self.product.category + '/' + str(self.product.id) + '/' + self.photo_path 
    
    
