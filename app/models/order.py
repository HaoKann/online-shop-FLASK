from app import db
from datetime import datetime, timezone

# order_product = db.Table('order_product',
#     db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
# )

class Order(db.Model):
    __tablename__='orders'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    date = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.Integer(), nullable=False, default=lambda: datetime.now(timezone.utc))
    price = db.Column(db.Integer())

    products_in_order = db.relationship('ProductInCart', backref='order', lazy='dynamic')


    # products = db.relationship('Product', secondary=order_product, backref='order')