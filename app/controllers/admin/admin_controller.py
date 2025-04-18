from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.forms.admin.add_product_form import AddProduct, CharacteristicsForm, PhotoForm
from app.forms.confirm_form import ConfirmForm
from app.forms.admin.edit_product_form import EditProduct
from app.models.product import Product, Characteristic, Photo
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

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
    products = db.paginate(db.session.query(Product), page=page, per_page=10, error_out=False)
    return render_template('admin/products_list.html', products=products.items)


@app.route('/admin/products/<int:id>', methods=['GET','POST'])
@login_required
def admin_product(id):
    if not current_user.is_admin:
        abort(403)
    сharacteristics_form = CharacteristicsForm(prefix='characteristics_form')
    photo_form = PhotoForm(prefix='photo_form')

    product = Product.query.get_or_404(id)

    if сharacteristics_form.validate_on_submit() and сharacteristics_form.submit_сharacteristics.data:
        сharacteristic = Characteristic(name=сharacteristics_form.name.data,
                                        int_value=сharacteristics_form.int_value.data, 
                                        str_value=сharacteristics_form.str_value.data, 
                                        prod_id=id )
        db.session.add(сharacteristic)
        db.session.commit()
        flash('Характеристика успешно добавлена!', 'succcess')
        return redirect(url_for('admin_product', id=id))
    
    if photo_form.validate_on_submit() and photo_form.submit_photo.data:
        f = photo_form.photo.data
        if f:
            photo_path = os.path.join(
                os.path.dirname(app.instance_path), 'app','static', 'products_photo', 
                product.category, str(product.id)
            )
            filename = secure_filename(f.filename)
            os.makedirs(photo_path, exist_ok=True)
            f.save(os.path.join( photo_path, filename ))
            photo = Photo(photo_path=filename,description=photo_form.description.data, prod_id=id )
            db.session.add(photo)
            db.session.commit()
            flash('Фото успешно добавлено', 'success')
            return redirect(url_for('admin_product', id=id))
    return render_template('admin/product_details.html', product=product, сharacteristics_form=сharacteristics_form, photo_form=photo_form)


@app.route('/admin/add_product', methods=['GET','POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        abort(403)
    form = AddProduct()

    if form.validate_on_submit():
        product = Product(name=form.name.data, category=form.category.data, price=form.price.data, discount=form.discount.data)
        db.session.add(product)
        db.session.commit()
        flash('Продукт успешно добавлен!', 'success')

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
    return render_template('admin/add_product.html', form=form)


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
