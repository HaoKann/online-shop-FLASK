from app import app
from flask import render_template
from flask_login import login_required

@app.route('/favourites')
@login_required
def favourites():
    return render_template('user/favourites.html')