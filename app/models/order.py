from app import db
from datetime import datetime, timezone

# order_product = db.Table('order_product',
#     db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
# )

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer())

    products_in_order = db.relationship('ProductInCart', backref='order', lazy='dynamic')
    delivery = db.relationship('Delivery', backref='order', uselist=False)
    user = db.relationship('User', back_populates='orders')

    # products = db.relationship('Product', secondary=order_product, backref='order')
    paid_products_in_order = db.relationship('ProductInOrder', backref='order', lazy='dynamic', cascade='all, delete-orphan')



class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.String(255))
    way_of_delivery = db.Column(db.String(255))
    time_of_arrival = db.Column(db.String(50))
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'))


class ProductInOrder(db.Model):
    __tablename__ = 'productsinorder'

    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)    
