from app import app
from flask import render_template

@app.route('/favourites')
def favourites():
    return render_template('user/favourites.html')