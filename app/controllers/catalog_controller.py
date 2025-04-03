from app import app
from flask import render_template

@app.route('/catalog')
def catalog():
    return render_template('main_screen/catalog.html')