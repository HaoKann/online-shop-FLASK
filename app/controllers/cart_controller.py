from app import db
from flask import render_template, redirect, flash, url_for, request, abort, jsonify, Blueprint
from app.models.product import Product
from app.models.cart import ProductInCart
from flask_login import login_required, current_user
from app.models.product import ReadyPC


cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def user_cart():
    return render_template('main_screen/cart.html', sub_title='Корзина')


@cart_bp.route('/cart/add_product/<int:product_id>', methods=['GET','POST'] )
@login_required
def add_products(product_id):

    product = Product.query.filter(Product.id == product_id, Product.is_active == True).first_or_404()

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

@cart_bp.route('/cart/add_ready_pc/<int:ready_pc_id>', methods=['GET','POST'])
@login_required
def add_ready_pc_to_cart(ready_pc_id):
    """
    Добавляет все товары из готовой сборки в корзину.
    """
    ready_pc = ReadyPC.query.get_or_404(ready_pc_id)

    # ИЗМЕНЕНИЕ: Добавляем .all() чтобы получить все товары из сборки
    for product_in_build in ready_pc.products_in_readypc.all():
        product_to_add = product_in_build.product
        
        existing_product_in_cart = ProductInCart.query.filter_by(
            product_id=product_to_add.id,
            cart_id=current_user.cart.id).first()

        if existing_product_in_cart:
            existing_product_in_cart.amount += 1
        else:
            new_product = ProductInCart(amount=1, product_id=product_to_add.id, cart_id=current_user.cart.id)
            db.session.add(new_product)
    
    db.session.commit()
    flash(f'Сборка "{ready_pc.name}" добавлена в корзину', 'success')
    return redirect(url_for('cart.user_cart'))

@cart_bp.route('/cart/delete_product/<int:product_id>', methods=['POST','DELETE'])
@login_required
def delete_products(product_id):
    try:
        deleted_product = ProductInCart.query.get_or_404(product_id)
        product_name = deleted_product.product.name
        db.session.delete(deleted_product)
        db.session.commit()
        flash(f'Продукт {product_name} удалён из корзины', 'danger')
        return jsonify({'message': f'Продукт {product_name} удален из корзины', 'status' : 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Ошибка при удалении продукта', 'status': 'error'}), 400


@cart_bp.route('/cart/increase_amount/<int:product_id>', methods=['POST']) # Изменен метод на POST
@login_required
def increase_amount(product_id):
    product_in_cart = ProductInCart.query.get_or_404(product_id)

    if product_in_cart.cart_id != current_user.cart.id:
        abort(403)
    
    product_in_cart.amount += 1
    db.session.commit()
    
    # ИЗМЕНЕНИЕ: Возвращаем JSON вместо redirect
    return jsonify({
        'status': 'success',
        'new_quantity': product_in_cart.amount,
        'item_total': product_in_cart.amount * product_in_cart.product.get_discount_price(),
        'cart_total': current_user.cart.sum_of_products_in_cart()
    })



@cart_bp.route('/cart/decrease_amount/<int:product_id>', methods=['POST'])
@login_required
def decrease_amount(product_id):
    product_in_cart = ProductInCart.query.get_or_404(product_id)

    if product_in_cart.cart_id != current_user.cart.id:
        abort(403)

    if product_in_cart.amount > 1:
        # Если товаров больше одного, просто уменьшаем количество
        product_in_cart.amount -= 1
        db.session.commit()
        return jsonify({
            'status': 'success',
            'new_quantity': product_in_cart.amount,
            'item_total': product_in_cart.amount * product_in_cart.product.get_discount_price(),
            'cart_total': current_user.cart.sum_of_products_in_cart()
        })
    else:
        # Если товар один, удаляем его
        product_name = product_in_cart.product.name
        db.session.delete(product_in_cart)
        db.session.commit()
        flash(f'Товар "{product_name}" был удален из корзины', 'success') # Добавляем flash-сообщение
        # ИЗМЕНЕНИЕ: Отправляем новый статус 'removed'
        return jsonify({
            'status': 'removed',
            'cart_total': current_user.cart.sum_of_products_in_cart()
        })