from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.forms.admin.add_product_form import AddProduct, CharacteristicsForm, PhotoForm
from app.forms.confirm_form import ConfirmForm
from app.forms.admin.edit_product_form import EditProduct
from app.models.product import Product, Characteristic, Photo
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.user import User
from app.forms.admin.edit_order import EditOrder

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    return render_template('admin/admin.html')

@app.route('/admin/products')
@login_required
def admin_products_list():
    if not current_user.is_admin:
        abort(403)
    page = request.args.get('page', 1, type=int)
    products = db.paginate(db.session.query(Product), page=page, per_page=20, error_out=False)
    return render_template('admin/products_list.html', products=products.items)


@app.route('/admin/products/<int:id>', methods=['GET','POST'])
@login_required
def admin_product(id):
    if not current_user.is_admin:
        abort(403)

    characteristics_form  = CharacteristicsForm(prefix='characteristics_form')
    photo_form = PhotoForm(prefix='photo_form')

    product = Product.query.get_or_404(id)

    if characteristics_form.validate_on_submit() and characteristics_form.submit_characteristics.data:
        characteristic = Characteristic(name=characteristics_form.name.data,
                                        int_value=characteristics_form.int_value.data, 
                                        str_value=characteristics_form.str_value.data, 
                                        prod_id=id )
        db.session.add(characteristic)
        db.session.commit()
        flash('Характеристика успешно добавлена!', 'succcess')
        return redirect(url_for('admin_product', id=id))
    
    if photo_form.validate_on_submit() and photo_form.submit_photo.data:
        f = photo_form.photo.data
        if f:
        # 1. Удаляем старое фото, если оно есть
            old_photo = Photo.query.filter_by(prod_id=id).first()
            if old_photo:
                old_photo_path = os.path.join(
                    os.path.dirname(app.instance_path), 'app', 'static', 'products_photo',
                    product.category, str(product.id), old_photo.photo_path
                )
                try:
                    os.remove(old_photo_path)
                except FileNotFoundError:
                    pass  # Если файла нет — просто пропускаем
                db.session.delete(old_photo)
                db.session.commit()

        # 2. Сохраняем новое фото
        photo_path = os.path.join(
            os.path.dirname(app.instance_path), 'app', 'static', 'products_photo',
            product.category, str(product.id)
        )
        filename = secure_filename(f.filename)
        os.makedirs(photo_path, exist_ok=True)
        f.save(os.path.join(photo_path, filename))

        # 3. Добавляем запись в БД
        photo = Photo(photo_path=filename, description=photo_form.description.data, prod_id=id)
        db.session.add(photo)
        db.session.commit()
        flash('Фото успешно заменено', 'success')
        return redirect(url_for('admin_product', id=id))
    return render_template('admin/product_details.html', product=product, сharacteristics_form=characteristics_form, photo_form=photo_form)

@app.route('/admin/add_product', methods=['GET','POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        abort(403)
    
    form = AddProduct()
    photo_form = PhotoForm()

    if form.validate_on_submit():
        # 1. Создаем продукт
        product = Product(
            name=form.name.data,
            category=form.category.data,
            price=form.price.data,
            discount=form.discount.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Продукт успешно добавлен!', 'success')

        # 2. Обработка фото (если оно было загружено)
        if photo_form.submit_photo.data and photo_form.photo.data:
            f = photo_form.photo.data
            if f:
                # Создаем папку для фото
                photo_dir = os.path.join(
                    os.path.dirname(app.instance_path),
                    'app', 'static', 'products_photo',
                    product.category, str(product.id)
                )
                os.makedirs(photo_dir, exist_ok=True)

                # Генерируем уникальное имя файла
                file_ext = os.path.splitext(f.filename)[1]
                filename = f"main{file_ext}"
                secure_name = secure_filename(filename)
                file_path = os.path.join(photo_dir, secure_name)

                # Сохраняем файл
                f.save(file_path)

                # Добавляем запись в БД
                photo = Photo(
                    photo_path=secure_name,
                    description=photo_form.description.data,
                    prod_id=product.id  # Используем ID созданного продукта
                )
                db.session.add(photo)
                db.session.commit()
                flash('Фото успешно добавлено', 'success')

        # 3. Редирект
        category_routes = {
            'gpu': 'graphics_card',
            'cpu': 'processor',
            'motherboard': 'motherboard',
            'psu': 'power_supply_unit',
            'ram': 'random_access_memory',
            'cooler': 'cooling_system',
            'storage': 'storage',
            'pc_case': 'computer_case',
        }
        route_name = category_routes.get(product.category, 'catalog')
        return redirect(url_for(route_name))

    return render_template('admin/add_product.html', form=form, photo_form=photo_form)



@app.route('/admin/edit_product/<int:id>', methods=['GET','POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        abort(403)
    edited_product = Product.query.get_or_404(id)

    form = EditProduct()

    if form.validate_on_submit():
        edited_product.name = form.name.data
        edited_product.category = form.category.data
        edited_product.price = form.price.data
        edited_product.discount = form.discount.data
        db.session.add(edited_product)
        db.session.commit()
        flash('Товар успешно изменён!', 'success')
        return redirect(url_for('admin_products_list'))
    form.name.data = edited_product.name
    form.category.data = edited_product.category
    form.price.data = edited_product.price
    form.discount.data = edited_product.discount
    return render_template('admin/edit_product.html', form=form, sub_title='Изменение товара')
        

@app.route('/admin/delete_product/<int:id>', methods=['GET','POST'])
@login_required
def admin_delete_products(id):
    if not current_user.is_admin:
        abort(403)

    deleted_product = Product.query.get_or_404(id)

    form = ConfirmForm()

    if form.validate_on_submit():
        db.session.delete(deleted_product)
        db.session.commit()
        flash('Товар удален успешно!','success')
        return redirect (url_for('admin_products_list'))
    return render_template('admin/admin_delete_product.html', form=form, sub_title = f'Вы точно хотите удалить продукт "{deleted_product.name}"?')

@app.route('/admin/user-orders')
@login_required
def all_user_orders():
    all_orders = Order.query.all()

    return render_template('admin/admin_orders.html', all_orders=all_orders)


@app.route('/admin/user-orders/delete/<int:id>', methods=['GET','POST'])
@login_required
def admin_delete_order(id):

    delete_order = Order.query.get_or_404(id)
    user = delete_order.user

    db.session.delete(delete_order)
    db.session.commit()
    flash(f'Заказ пользователя {user.name} удалён!', 'success')
    return redirect(url_for('all_user_orders'))

@app.route('/admin/user-orders/edit/<int:id>', methods=['GET','POST'])
@login_required
def admin_edit_order(id):

    edit_order = Order.query.get_or_404(id)
    user = edit_order.user

    form = EditOrder()

    if form.validate_on_submit():
        edit_order.user.phone_number = form.phone_number.data
        edit_order.user.email = form.email.data
        edit_order.delivery.address = form.address.data
        edit_order.delivery.way_of_delivery = form.way_of_delivery.data
        edit_order.delivery.time_of_arrival = form.time_of_arrival.data
        db.session.add(edit_order)
        db.session.commit()
        flash(f'Заказ пользователя {user.name} успешно изменён!', 'success')
        return redirect(url_for('all_user_orders'))
    form.phone_number.data = edit_order.user.phone_number
    form.email.data = edit_order.user.email
    form.address.data = edit_order.delivery.address
    form.way_of_delivery.data = edit_order.delivery.way_of_delivery
    form.way_of_delivery.data = edit_order.delivery.time_of_arrival
    return render_template('admin/admin_edit_order.html', form=form)



@app.route('/admin/ready-pcs')
@login_required
def admin_ready_pcs():
    return render_template('admin/admin_ready_pcs.html')


@app.route('/admin/add/ready-pc', methods=['GET','POST'])
@login_required
def admin_add_readypc():
    return render_template('admin/admin_add_readypc.html')


