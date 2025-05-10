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
        result = db.session.query(Product).filter(Product.name.ilike(f'%{q}%')).all()

    return render_template('search/search.html', result=result, q=q)