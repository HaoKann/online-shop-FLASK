from app import app, db
from flask import flash, render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from app.forms.order_form import UserOrderForm
from app.models.order import Order, Delivery
from app.models.cart import ProductInCart

@app.route('/user-orders', methods=['GET','POST'])
@login_required
def show_orders():
    # Загружаем заказы, где user_id совпадает с ID текущего пользователя
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    return render_template('user/user_orders.html', all_orders=user_orders)


@app.route('/order', methods=['GET','POST'])
@login_required
def make_order():
    
    form = UserOrderForm()
    
    if not current_user.cart.products_in_cart.count():
        flash('В корзине нет товаров!', 'danger')
        return redirect(url_for('user_cart'))

    if form.validate_on_submit():
        try:
            # Создаем заказ с начальным статусом
            new_order = Order(user_id=current_user.id, price=current_user.cart.sum_of_products_in_cart(), status='pending')
            db.session.add(new_order)
            # Важно: сначала "смываем" изменения, чтобы получить new_order.id
            db.session.flush()

            # Создаем информацию о доставке
            delivery = Delivery(address=form.address.data, way_of_delivery=form.way_of_delivery.data, 
                time_of_arrival=form.time_of_arrival.data, order_id=new_order.id
            )
            db.session.add(delivery)

            # Перемещаем товары из корзины в заказ
            for product_in_cart in current_user.cart.products_in_cart.all():
                product_in_cart.cart_id = None # Отвязываем от корзины
                product_in_cart.order_id = new_order.id # Привязываем к новому заказу

            # Делаем ТОЛЬКО ОДИН commit в самом конце
            db.session.commit()

        
          # --- КОНЕЦ ТРАНЗАКЦИИ ---
            
            flash('Заказ успешно оформлен!','success')
            # 4. Делаем REDIRECT на страницу заказов
            return redirect(url_for('show_orders'))
        
        except Exception as e:
            db.session.rollback() # Откатываем все изменения в случае ошибки
            flash(f'Произошла ошибка при оформлении заказа: {e}', 'danger')
            return redirect(url_for('user_cart'))
        
    return render_template('user/order.html', form=form, 
                           stripe_publishable_key = current_app.config['STRIPE_PUBLISHABLE_KEY'])

@app.route('/order-success')
@login_required
def order_success():
    # Здесь должна быть логика очистки корзины и т.д.
    flash('Оплата прошла успешно!', 'success')
    return render_template('user/order_success.html') # Нужно создать этот шаблон


@app.route('/user-orders/details/<int:order_id>', methods=['GET','POST'])
@login_required
def user_order_details(order_id):
    # Ищем заказ, у которого ID совпадает с order_id И user_id совпадает с ID текущего пользователя
    user_order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('user/order_details.html', user_order=user_order)
