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
        
    def get_discount_price(self):
        if self.discount:
            discount_price = self.price * self.discount / 100
            total_price = self.price - discount_price
            return round(total_price)
        else:
            return self.price
        

    def get_category_name(self):
        category_map = {
            'gpu': 'Видеокарта',
            'cpu': 'Процессор',
            'motherboard': 'Материнская плата',
            'ram': 'Оперативная память',
            'psu': 'Блок питания',
            'cooler': 'Система охлаждения',
            'storage': 'Накопитель',
            'pc_case': 'Корпус',
        }
        return category_map.get(self.category, self.category)


ready_pc_products = db.Table('ready_pc_products',
    db.Column('readypc_id', db.Integer, db.ForeignKey('readypc.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)

class ReadyPC(db.Model):
    __tablename__='readypc'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)

    products = db.relationship('Product', secondary='ready_pc_products', backref='ready_pcs' )




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
    
    
