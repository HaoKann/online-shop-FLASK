from app import db
from flask import render_template, request, flash, Blueprint
from app.models.product import Product

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods = ['GET','POST'])
def search():
    q = request.args.get('q')
    if not q:
        result = []
        flash('Неправильно введеный запрос', 'danger')
    else:
        words = q.split(' ')
        # Начинаем запрос с фильтра по активным товарам
        query = db.session.query(Product).filter(Product.is_active == True)

        # Добавляем фильтры для каждого слова в запросе
        for word in words:
            query = query.filter(Product.name.ilike(f'%{word}%'))
            
        result = query.all()    
    return render_template('search/search.html', result=result, q=q)


@search_bp.route('/admin/search', methods = ['GET','POST'])
def admin_search():
    q = request.args.get('q')
    if not q:
        result = []
        flash('Неправильно введеный запрос', 'danger')
    else:
        words = q.split(' ')
        result = db.session.query(Product).filter(Product.name.ilike(f'%{words[0]}%'))
        for word in words[1:]:
            result = result.filter(Product.name.ilike(f'%{word}%'))
        result = result.all()    
    return render_template('admin/admin_search.html', result=result, q=q)