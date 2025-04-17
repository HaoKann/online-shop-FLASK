from app import app
from flask import render_template
from flask_login import login_required

@app.route('/user-orders')
@login_required
def user_orders():
    return render_template('user/user_orders.html')