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

    def sum_of_products_in_cart(self):

        sum_of_products = 0

        for product_in_cart in self.products_in_cart.all():
            sum_of_products += product_in_cart.amount * product_in_cart.product.price
        return sum_of_products

    def sum_of_products_amount(self):

        prod_amount = 0

        for product_in_cart in self.products_in_cart.all():
            if product_in_cart.amount > 0:
                prod_amount += product_in_cart.amount
        return prod_amount



class ProductInCart(db.Model):
    __tablename__='productsincart'

    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer(), default=1)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    cart_id = db.Column(db.Integer(), db.ForeignKey('carts.id'))
    

