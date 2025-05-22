from app import app, db
from flask import flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.forms.order_form import OrderForm
from app.models.order import Order


@app.route('/user-orders', methods=['GET','POST'])
@login_required
def show_orders():
    all_orders  = Order.query.all()
    return render_template('user/user_orders.html', all_orders=all_orders)


@app.route('/order', methods=['GET','POST'])
@login_required
def make_order():
    
    form = OrderForm()
    
    if not current_user.cart.products_in_cart.count():
        flash('В корзине нет товаров!', 'danger')
        return redirect(url_for('user_cart'))

    if form.validate_on_submit():
        order = Order(user_id=current_user.id, price=current_user.cart.sum_of_products_in_cart())
        db.session.add(order)
        db.session.commit()

        for product_in_cart in current_user.cart.products_in_cart.all():
            product_in_cart.cart_id = None
            product_in_cart.order_id = order.id
        db.session.commit()
        
        address = form.address.data
        way_of_delivery = form.way_of_delivery.data
        time_of_arrival = form.time_of_arrival.data

    
        flash('Заказ успешно оформлен!','success')
    return render_template('user/order.html',form=form)