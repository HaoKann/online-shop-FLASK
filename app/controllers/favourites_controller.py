from app import app,db
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.user import FavouriteProduct

@app.route('/favourites')
@login_required
def favourites():
    favourite_products = FavouriteProduct.query.filter_by(user_id=current_user.id).all()
    return render_template('user/favourites.html', sub_title='Избранное', favourite_products=favourite_products)


@app.route('/favourites/add_product/<int:product_id>', methods=['GET','POST'])
@login_required
def add_to_favourites(product_id):
    
    product = Product.query.get_or_404(product_id)

    already_in_favourite = FavouriteProduct.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if already_in_favourite:
        flash(f'Товар {product.name} уже добавлен в избранное', 'warning')
        return redirect(url_for('favourites'))
    
    new_favourite_product = FavouriteProduct(user_id = current_user.id, product_id=product.id)
    db.session.add(new_favourite_product)
    db.session.commit()

    flash(f'Товар {product.name} добавлен в избранное', 'success')
    return redirect(url_for('favourites'))


    