from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.models.product import Product
from app.models.cart import Cart, ProductInCart
from flask_login import login_required, current_user
from app.forms.confirm_form import ConfirmForm

@app.route('/cart')
@login_required
def user_cart():
    return render_template('main_screen/cart.html', sub_title='Корзина')


@app.route('/cart/add_product/<int:product_id>', )
@login_required
def add_products(product_id):

    product = Product.query.get_or_404(product_id)

    # Проверка есть ли уже такой товар в корзине текущего пользователя
    existing_product = ProductInCart.query.filter_by(
        product_id=product.id,
        cart_id=current_user.cart.id).first()

    if existing_product:
        existing_product.amount += 1
    else:
        new_product = ProductInCart(amount=1, product_id=product.id, cart_id=current_user.cart.id)
        db.session.add(new_product)

    db.session.commit()
    flash(f'Товар {product.name} добавлен в корзину', 'success')
    return redirect(request.referrer or '/')

@app.route('/cart/delete_product/<int:product_id>', methods=['GET','POST'])
@login_required
def delete_products(product_id):
    
    form = ConfirmForm()
    deleted_product = ProductInCart.query.get_or_404(product_id)

    product_name = deleted_product.product.name

    if form.validate_on_submit():
        db.session.delete(deleted_product)
        db.session.commit()
        flash(f'Продукт {product_name} удалён из корзины', 'info')
        return redirect(url_for('user_cart'))
    return render_template('main_screen/confirm.html', form=form, sub_title=f'Вы точно хотите удалить {product_name}?' )