from app import app
from flask import render_template

@app.route('/user-orders')
def user_orders():
    return render_template('user/user_orders.html')