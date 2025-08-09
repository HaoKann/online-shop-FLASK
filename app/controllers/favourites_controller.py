from app import db
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.user import FavouriteProduct
from app.models.cart import ProductInCart

favourites_bp = Blueprint('favourites', __name__)

@favourites_bp.route('/favourites')
@login_required
def favourites():
    favourite_products = FavouriteProduct.query.filter_by(user_id=current_user.id).all()
    return render_template('user/favourites.html', sub_title='Избранное', favourite_products=favourite_products)


@favourites_bp.route('/favourites/add_product/<int:product_id>', methods=['GET','POST'])
@login_required
def add_to_favourites(product_id):
    
    product = Product.query.get_or_404(product_id)

    already_in_favourite = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if already_in_favourite:
        flash(f'Товар {product.name} уже добавлен в избранное', 'warning')
        return redirect(url_for('favourites'))
    
    new_favourite_product = FavouriteProduct(user_id = current_user.id, product_id=product.id)
    db.session.add(new_favourite_product)
    db.session.commit()

    flash(f'Товар {product.name} добавлен в избранное', 'success')
    return redirect(url_for('favourites'))

@favourites_bp.route('/favourites/delete_product/<int:product_id>', methods=['GET','POST'])
@login_required
def delete_product_from_favourites(product_id):
    
    favourite_product = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if favourite_product:
        product_name = favourite_product.product.name # сохраняю имя продукта до удаления
        db.session.delete(favourite_product)
        db.session.commit()
        flash(f'Товар {product_name} удален из избранного','warning')
    else:
        flash('Товар не найден в избранном', 'danger')
    
    return redirect(url_for('favourites'))


@favourites_bp.route('/favourites/add_product_to_cart/<int:product_id>', methods=['GET','POST'])
@login_required
def add_favourite_product_to_cart(product_id):

    # Проверка наличия товара в избранном
    favourite_product = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not favourite_product:
       flash('Товар не найден', 'warning')
       return redirect(url_for('favourites')) 
    
    # Проверка наличия товара в корзине
    product_in_cart  = ProductInCart.query.filter_by(cart_id=current_user.cart.id, product_id=product_id).first()

    if product_in_cart:
        product_in_cart.amount += 1
        flash(f'Товар {favourite_product.product.name} уже есть в корзине', 'info')
    else:
        new_product_in_cart = ProductInCart(cart_id=current_user.cart.id, product_id=product_id, amount=1)
        db.session.add(new_product_in_cart)
        flash(f'Товар {favourite_product.product.name} был добавлен в корзину', 'success')
    
    db.session.commit()
    return redirect(url_for('user_cart'))



