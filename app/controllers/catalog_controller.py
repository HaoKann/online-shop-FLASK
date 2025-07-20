from app import app
from flask import render_template, request
from app.models.product import Product


@app.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    all_products_in_catalog = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('main_screen/catalog.html', products=all_products_in_catalog, active_page = 'catalog')

@app.route('/gpu')
def graphics_card():
    page = request.args.get('page', 1, type=int)
    gpu_products = Product.query.filter_by(category='gpu').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html', sub_title ='Видеокарты', products=gpu_products, endpoint='graphics_card')

@app.route('/cpu')
def processor():
    page = request.args.get('page', 1, type=int)
    processor_products = Product.query.filter_by(category='cpu').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Процессоры', products=processor_products, endpoint='processor')

@app.route('/motherboard')
def motherboard():
    page = request.args.get('page', 1, type=int)
    motherboard_products = Product.query.filter_by(category='motherboard').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Материнские платы', products=motherboard_products,endpoint='motherboard')

@app.route('/psu')
def power_supply_unit():
    page = request.args.get('page', 1, type=int)
    psu_products = Product.query.filter_by(category='psu').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Блоки питания', products=psu_products,endpoint='power_supply_unit')

@app.route('/ram')
def random_access_memory():
    page = request.args.get('page', 1, type=int)
    ram_products = Product.query.filter_by(category='ram').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Оперативная память', products=ram_products,endpoint='random_access_memory')

@app.route('/cooler')
def cooling_system():
    page = request.args.get('page', 1, type=int)
    cooler_products = Product.query.filter_by(category='cooler').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Кулеры и системы охлаждения', products=cooler_products,endpoint='cooling_system')

@app.route('/storage')
def storage():
    page = request.args.get('page', 1, type=int)
    storage_products = Product.query.filter_by(category='storage').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Жесткие диски и твердотельные накопители', products=storage_products,endpoint='storage')

@app.route('/pc_case')
def computer_case():
    page = request.args.get('page', 1, type=int)
    case_products = Product.query.filter_by(category='pc_case').paginate(page=page, per_page=10)
    return render_template('catalog/products_in_catalog.html',sub_title='Корпуса', products=case_products,endpoint='computer_case')


@app.route('/product_details/<int:prod_id>')
def show_prod_details(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('catalog/product_details.html', product=product)

