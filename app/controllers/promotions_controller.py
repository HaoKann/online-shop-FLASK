from flask import render_template, Blueprint
from app.models.product import Product

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/promotions')
def promotions():

    discounted_products = Product.query.filter(Product.discount > 0, Product.is_active == True).all()

    return render_template('main_screen/promotions.html', sub_title='Акции', discounted_products=discounted_products)