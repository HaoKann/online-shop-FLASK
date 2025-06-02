from app import app
from flask import render_template
from app.models.product import Product

@app.route('/products')
def all_products():
    return render_template('catalog/all_products.html')

@app.route('/catalog')
def catalog():
    return render_template('main_screen/catalog.html')

@app.route('/gpu')
def graphics_card():
    gpu_products = Product.query.filter_by(category='gpu').all()
    return render_template('catalog/products_in_catalog.html', sub_title ='Видеокарты', products=gpu_products)

@app.route('/cpu')
def processor():
    processor_products = Product.query.filter_by(category='cpu').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Процессоры', products=processor_products)

@app.route('/motherboard')
def motherboard():
    motherboard_products = Product.query.filter_by(category='motherboard').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Материнские платы', products=motherboard_products)

@app.route('/psu')
def power_supply_unit():
    psu_products = Product.query.filter_by(category='psu').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Блоки питания', products=psu_products)

@app.route('/ram')
def random_access_memory():
    ram_products = Product.query.filter_by(category='ram').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Оперативная память', products=ram_products)

@app.route('/cooler')
def cooling_system():
    cooler_products = Product.query.filter_by(category='cooler').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Кулеры и системы охлаждения', products=cooler_products)

@app.route('/storage')
def storage():
    storage_products = Product.query.filter_by(category='storage').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Жесткие диски и твердотельные накопители', products=storage_products)

@app.route('/pc_case')
def computer_case():
    case_products = Product.query.filter_by(category='pc_case').all()
    return render_template('catalog/products_in_catalog.html',sub_title='Корпуса', products=case_products)


@app.route('/product_details/<int:prod_id>')
def show_prod_details(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('catalog/product_details.html', product=product)

