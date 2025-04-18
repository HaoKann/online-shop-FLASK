from app import db

# промежуточная таблица cart_products
# cart_products = db.Table('cart_products', 
#     db.Column('cart_id', db.Integer, db.ForeignKey('carts.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
# )

class Cart(db.Model):
    __tablename__='carts'

    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    # secondary=cart_products — указывает, что связь через промежуточную таблицу
    # products = db.relationship('Product', secondary=cart_products, backref='cart')

    products_in_cart = db.relationship('ProductInCart', backref='cart', lazy='dynamic')


class ProductInCart(db.Model):
    __tablename__='productsincart'

    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer(), default=1)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
    cart_id = db.Column(db.Integer(), db.ForeignKey('carts.id'))
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'))

