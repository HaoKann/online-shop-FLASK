from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms.admin.add_product_form import AddProduct
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