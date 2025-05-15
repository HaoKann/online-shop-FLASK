from app import app
from flask import render_template

@app.route('/promotions')
def promotions():
    return render_template('main_screen/promotions.html', sub_title='Акции')