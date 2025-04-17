from app import app
from flask import render_template
from flask_login import login_required

@app.route('/user')
@login_required
def user():
    return render_template('user/userpage.html')