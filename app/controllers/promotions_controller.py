from flask import render_template, Blueprint, request
from app.models.product import Product
from app.forms.empty_form import EmptyForm
from app.controllers.catalog_controller import apply_sorting

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/promotions')
def promotions():

    query = Product.query.filter(Product.is_active == True, Product.discount > 0)
    query = apply_sorting(query)
    discounted_products = query.all()

    current_sort = request.args.get('sort', 'newest')
    csrf_form = EmptyForm() 
    
    return render_template('main_screen/promotions.html', sub_title='Акции', current_sort=current_sort, discounted_products=discounted_products, csrf_form=csrf_form)