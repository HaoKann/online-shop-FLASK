from app import app
from flask import render_template
from app.forms.admin.add_product_form import AddProduct

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')

@app.route('/admin/products_list')
def admin_products_list():
    return render_template('/admin/products_list.html')

@app.route('/admin/add_product')
def admin_add_product():
    form = AddProduct()


    return render_template('admin/add_product.html', form=form)