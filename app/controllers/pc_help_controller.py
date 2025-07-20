from app import app
from flask import render_template
from flask_login import login_required

@app.route('/pc_help')
@login_required
def pc_help():
    return render_template('main_screen/pc_help.html')