from app import app
from flask import render_template

@app.route('/user')
def user():
    return render_template('user/userpage.html')