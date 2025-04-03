from app import app
from flask import render_template

@app.route('/pc_help')
def pc_help():
    return render_template('main_screen/pc_help.html')