from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.models.product import Product
from app.models.cart import Cart, ProductInCart
from flask_login import login_required, current_user

@app.route('/cart')
@login_required
def user_cart():
    return render_template('main_screen/cart.html', sub_title='Корзина')


@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_product(product_id):

    product = Product.query.get_or_404(product_id)
    product_in_cart = ProductInCart(amount=1, product_id=product.id, cart_id=current_user.cart.id)
    db.session.add(product_in_cart)
    db.session.commit()
    flash(f'Товар {product.name} добавлен в корзину', 'success')
    return redirect(request.referrer or '/')
