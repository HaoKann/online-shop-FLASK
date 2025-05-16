from app import app
from flask import render_template
from app.models.product import Product

@app.route('/promotions')
def promotions():

    discounted_products = Product.query.filter(Product.discount > 0).all()

    return render_template('main_screen/promotions.html', sub_title='Акции', discounted_products=discounted_products)