from app import app, db
from flask import render_template
from app.models.product import Product

@app.route('/catalog')
def catalog():
    return render_template('main_screen/catalog.html')

@app.route('/gpu')
def graphics_card():
    gpu_products = Product.query.filter_by(category='gpu').all()
    return render_template('catalog/gpu.html', sub_title ='Видеокарты', products=gpu_products)

@app.route('/cpu')
def processor():
    return render_template('catalog/cpu.html',sub_title='Процессоры')

@app.route('/motherboard')
def motherboard():
    return render_template('catalog/motherboard.html',sub_title='Материнские платы ')

@app.route('/psu')
def power_supply_unit():
    return render_template('catalog/psu.html',sub_title='Блоки питания')

@app.route('/ram')
def random_access_memory():
    return render_template('catalog/ram.html',sub_title='Оперативная память')

@app.route('/cooler')
def cooling_system():
    return render_template('catalog/cooler.html',sub_title='Кулеры и системы охлаждения ')

@app.route('/storage')
def storage():
    return render_template('catalog/storage.html',sub_title='Жесткие диски и твердотельные накопители')

@app.route('/pc_case')
def computer_case():
    return render_template('catalog/pc_case.html',sub_title='Корпуса')

