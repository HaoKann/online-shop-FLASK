from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms.admin.add_product_form import AddProduct
from app.forms.confirm_form import ConfirmForm
from app.forms.admin.edit_product_form import EditProduct
from app.models.product import Product

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/products')
def admin_products_list():
    page = int(request.args.get('page', 1))
    products = db.paginate(db.session.query(Product), page=page, per_page=10, error_out=False)
    print(page)
    return render_template('admin/products_list.html', products=products.items)


@app.route('/admin/products/<int:id>')
def admin_product(id):
    product = Product.query.get_or_404(id)
    return render_template('admin/product_details.html', product=product)


@app.route('/admin/add_product', methods=['GET','POST'])
def admin_add_product():
    form = AddProduct()

    if form.validate_on_submit():
        product = Product(name=form.name.data, category=form.category.data, price=form.price.data, discount=form.discount.data)
        db.session.add(product)
        db.session.commit()
        flash('Продукт успешно добавлен!', 'success')
        return redirect(url_for('admin_product', id=product.id))
    return render_template('admin/add_product.html', form=form)


@app.route('/admin/edit_product/<int:id>', methods=['GET','POST'])
def admin_edit_product(id):
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
def admin_delete_products(id):
    deleted_product = Product.query.get_or_404(id)

    form = ConfirmForm()

    if form.validate_on_submit():
        db.session.delete(deleted_product)
        db.session.commit()
        flash('Товар удален успешно!','success')
        return redirect (url_for('admin_products_list'))
    return render_template('admin/admin_delete_product.html', form=form, sub_title = f'Вы точно хотите удалить продукт "{deleted_product.name}"?')
