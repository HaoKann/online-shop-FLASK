from flask import render_template, Blueprint
from app.models.about import Milestone
from app.models.product import Product
from app.models.faq import FAQ
# defaultdict - продвинутый вид словаря, если обращаться к ключу которого еще не существует 
# он автоматически создает ключ со значением "по умолчанию" которое я задал
# обычный словарь dict выдаст ошибку KeyError
from collections import defaultdict


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


@main_bp.route('/faq')
def faq():
    # Загружаем все вопросы, отсортированные по категории
    # Это сортировка всех найденных строк по алфавиту на основе значений в колонке category 
    faqs_from_db = FAQ.query.order_by(FAQ.category).all() 

    # Группируем вопросы по категориям в словарь
    grouped_faqs = defaultdict(list)
    for faq_item in faqs_from_db:
        grouped_faqs[faq_item.category].append(faq_item)

    return render_template('main_screen/faq.html', grouped_faqs=grouped_faqs, subtitle='Часто задаваемые вопросы')