from flask import render_template, request, Blueprint
from app.models.product import Product
from app.models.product import Category
from app.forms.empty_form import EmptyForm

# 1. Создаем Blueprint
catalog_bp = Blueprint('catalog', __name__)

# 2. Используем Blueprint для создания маршрутов

@catalog_bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    all_products_in_catalog = Product.query.filter(Product.is_active == True).paginate(page=page, per_page=per_page, error_out=False)
    
    csrf_form = EmptyForm()

    return render_template('main_screen/catalog.html', products=all_products_in_catalog, active_page = 'catalog', csrf_form=csrf_form)

@catalog_bp.route('/gpu')
def graphics_card():
    page = request.args.get('page', 1, type=int)
    gpu_products = Product.query.join(Category).filter(Category.slug == 'gpu', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()

    return render_template('catalog/products_in_catalog.html', sub_title ='Видеокарты', products=gpu_products, endpoint='graphics_card',csrf_form=csrf_form)

@catalog_bp.route('/cpu')
def processor():
    page = request.args.get('page', 1, type=int)
    processor_products = Product.query.join(Category).filter(Category.slug == 'cpu', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Процессоры', products=processor_products, endpoint='processor',csrf_form=csrf_form)

@catalog_bp.route('/motherboard')
def motherboard():
    page = request.args.get('page', 1, type=int)
    motherboard_products = Product.query.join(Category).filter(Category.slug == 'motherboard', Product.is_active == True).paginate(page=page, per_page=10)
   
    csrf_form = EmptyForm()

    return render_template('catalog/products_in_catalog.html',sub_title='Материнские платы', products=motherboard_products,endpoint='motherboard',csrf_form=csrf_form)

@catalog_bp.route('/psu')
def power_supply_unit():
    page = request.args.get('page', 1, type=int)
    psu_products = Product.query.join(Category).filter(Category.slug == 'psu', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Блоки питания', products=psu_products,endpoint='power_supply_unit',csrf_form=csrf_form)

@catalog_bp.route('/ram')
def random_access_memory():
    page = request.args.get('page', 1, type=int)
    ram_products = Product.query.join(Category).filter(Category.slug == 'ram', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Оперативная память', products=ram_products,endpoint='random_access_memory',csrf_form=csrf_form)

@catalog_bp.route('/cooler')
def cooling_system():
    page = request.args.get('page', 1, type=int)
    cooler_products = Product.query.join(Category).filter(Category.slug == 'cooler', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Кулеры и системы охлаждения', products=cooler_products,endpoint='cooling_system',csrf_form=csrf_form)

@catalog_bp.route('/storage')
def storage():
    page = request.args.get('page', 1, type=int)
    storage_products = Product.query.join(Category).filter(Category.slug == 'storage', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Жесткие диски и твердотельные накопители', products=storage_products,endpoint='storage',csrf_form=csrf_form)

@catalog_bp.route('/pc_case')
def computer_case():
    page = request.args.get('page', 1, type=int)
    case_products = Product.query.join(Category).filter(Category.slug == 'pc_case', Product.is_active == True).paginate(page=page, per_page=10)
    
    csrf_form = EmptyForm()
    
    return render_template('catalog/products_in_catalog.html',sub_title='Корпуса', products=case_products,endpoint='computer_case',csrf_form=csrf_form)


@catalog_bp.route('/product_details/<int:prod_id>')
def show_prod_details(prod_id):
    product = Product.query.filter(Product.id == prod_id, Product.is_active == True).first_or_404()

    # Получаем ШАБЛОН обязательных характеристик
    required_specs_template = []
    if product.category:
        required_specs_template = product.category.required_characteristics.order_by('id').all()

    # Создаем словарь существующих, заполненных значений
    existing_spec_value = {spec.name: spec.value for spec in product.characteristics}

    return render_template('catalog/product_details.html', product=product, required_specs=required_specs_template, spec_values=existing_spec_value)

