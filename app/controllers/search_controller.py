from app import app, db
from flask import render_template, request, flash
from app.models.product import Product

@app.route('/search', methods = ['GET','POST'])
def search():
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
    return render_template('search/search.html', result=result, q=q)


@app.route('/admin/search', methods = ['GET','POST'])
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