from flask import render_template, Blueprint
from app.models.about import Milestone
from app.models.product import Product

# 1. Создаем Blueprint для этой "главы"
main_bp = Blueprint('main', __name__)

# 2. Используем Blueprint для создания маршрутов
@main_bp.route('/')
def main():
    latest_products = Product.query.order_by(Product.id.desc()).limit(6).all()
    return render_template('main.html', products_for_showcase = latest_products)


@main_bp.route('/about')
def about():
    milestones = Milestone.query.order_by(Milestone.year.asc()).all()
    return render_template('main_screen/about.html', milestones=milestones)