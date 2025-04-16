from app import app
from flask import render_template, url_for
from app.models.product import Product
from app.models.cart import Cart, ProductInCart

@app.route('/cart')
def user_cart():
    # cart = Cart.query.filter_by(user_id=current_user.id).first()

    return render_template('main_screen/cart.html')
