from app import app, db
from flask import flash, render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from app.forms.order_form import UserOrderForm
from app.models.order import Order, Delivery
from app.models.cart import ProductInCart
from datetime import datetime
from flask_wtf import FlaskForm

class EmptyForm(FlaskForm):
    pass

@app.route('/user-orders', methods=['GET','POST'])
@login_required
def show_orders():
    # Загружаем заказы, где user_id совпадает с ID текущего пользователя
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    return render_template('user/user_orders.html', all_orders=user_orders)


@app.route('/order', methods=['GET','POST'])
@login_required
def make_order():
    # Этот маршрут теперь просто готовит страницу для оплаты
    if not current_user.cart.products_in_cart.count():
        flash('Ваша корзина пуста!', 'danger')
        return redirect(url_for('user_cart'))
    
    # ДОБАВЛЯЕМ СТРОКУ ДЛЯ ПРОВЕРКИ
    print(f"DEBUG: Ключ Stripe в контроллере: {current_app.config.get('STRIPE_PUBLISHABLE_KEY')}")
    
    form = EmptyForm()
    # Просто отображаем страницу оплаты, передавая в нее публичный ключ
    return render_template('checkout.html', # Используем шаблон с формой Stripe
                           stripe_publishable_key=current_app.config['STRIPE_PUBLISHABLE_KEY'], form=form)

@app.route('/order-success')
@login_required
def order_success():
    try:
        # 1. Создаем сам заказ, ТЕПЕРЬ мы уверены, что он оплачен
        new_order = Order(
            user_id=current_user.id,
            price=current_user.cart.sum_of_products_in_cart(),
            status='pending', # Начальный статус "в обработке"
            date=datetime.utcnow()
        )
        db.session.add(new_order)
        db.session.flush() # Это нужно, чтобы получить new_order.id до коммита

        # 2. Перемещаем товары из корзины в заказ
        cart_items = current_user.cart.products_in_cart.all()
        for item in cart_items:
            # Удаляем товар из корзины
            db.session.delete(item)
        
        # 3. Сохраняем все изменения (новый заказ и пустую корзину)
        db.session.commit()
        flash('Оплата прошла успешно! Ваш заказ оформлен.', 'success')

    except Exception as e:
        db.session.rollback() # Если что-то пошло не так, откатываем все
        flash(f'Произошла ошибка при сохранении заказа: {e}', 'danger')

    return render_template('user/order_success.html')
   


@app.route('/user-orders/details/<int:order_id>', methods=['GET','POST'])
@login_required
def user_order_details(order_id):
    # Ищем заказ, у которого ID совпадает с order_id И user_id совпадает с ID текущего пользователя
    user_order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('user/order_details.html', user_order=user_order)
