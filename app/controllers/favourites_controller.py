from app import db
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_required, current_user
from app.models.product import Product, ReadyPC
from app.models.user import FavouriteProduct
from app.models.cart import ProductInCart
from app.forms.empty_form import EmptyForm

favourites_bp = Blueprint('favourites', __name__)

@favourites_bp.route('/favourites')
@login_required
def favourites():
    # 1. Добавляем .all(), чтобы выполнить запрос и получить список
    # 2. Оптимизируем запрос, чтобы он подтягивал и Product, и ReadyPC
    favourite_items_list = FavouriteProduct.query.outerjoin(Product).filter(
        FavouriteProduct.user_id == current_user.id,
        (Product.is_active == True) | (FavouriteProduct.product_id == None)
    ).all()

    csrf_form = EmptyForm()
    
    # 3. ВАЖНО: передаем переменную под тем именем, которое ждет HTML-шаблон (favourite_products)
    return render_template('user/favourites.html', sub_title='Избранное', favourite_products=favourite_items_list, csrf_form=csrf_form)


# --- УНИВЕРСАЛЬНЫЙ МАРШРУТ ДОБАВЛЕНИЯ ---
@favourites_bp.route('/favourites/add_product/<int:product_id>', methods=['GET','POST'])
@favourites_bp.route('/favourites/add_ready_pc/<int:ready_pc_id>', methods=['GET','POST'])
@login_required
def add_to_favourites(product_id = None, ready_pc_id = None):
    
    if product_id:
        item = Product.query.get_or_404(product_id)
        already_in_favourite = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        # Готовим объект для сохранения (только если нет в избранном)
        if not already_in_favourite:
            new_fav = FavouriteProduct(user_id=current_user.id, product_id=product_id)

    elif ready_pc_id:
        item = ReadyPC.query.get_or_404(ready_pc_id)
        # Проверяем наличие именно сборки в избранном
        already_in_favourite = FavouriteProduct.query.filter_by(user_id=current_user.id, ready_pc_id=ready_pc_id).first()
        if not already_in_favourite:
            new_fav = FavouriteProduct(user_id=current_user.id, ready_pc_id=ready_pc_id)

    else:
        flash('Товар не найден', 'danger')
        return redirect(url_for('catalog.catalog'))
    
    if already_in_favourite:
        flash(f'{item.name} уже добавлен в избранное', 'warning')
        return redirect(request.referrer or url_for('favourites.favourites'))

    db.session.add(new_fav)
    db.session.commit()    

    flash(f'{item.name} добавлен в избранное', 'success')
    return redirect(request.referrer or url_for('favourites.favourites'))


@favourites_bp.route('/favourites/delete_product/<int:product_id>', methods=['GET','POST'])
@favourites_bp.route('/favourites/delete_ready_pc/<int:ready_pc_id>', methods=['GET','POST'])
@login_required
def delete_product_from_favourites(product_id = None, ready_pc_id = None):
    
    if product_id:
        fav = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    elif ready_pc_id:
        fav = FavouriteProduct.query.filter_by(user_id=current_user.id, ready_pc_id=ready_pc_id).first()

    if fav:
        name = fav.product.name if fav.product else fav.ready_pc.name
        db.session.delete(fav)
        db.session.commit()
        flash(f'{name} удален из избранного','warning')
    else:
        flash('Товар не найден в избранном', 'danger')
    
    return redirect(url_for('favourites.favourites'))



@favourites_bp.route('/favourites/add_product_to_cart/<int:product_id>', methods=['GET','POST'])
@login_required
def add_favourite_product_to_cart(product_id):

    # Проверка наличия товара в избранном
    favourite_product = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not favourite_product:
       flash('Товар не найден', 'warning')
       return redirect(url_for('favourites.favourites')) 
    
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
    return redirect(url_for('cart.user_cart'))



