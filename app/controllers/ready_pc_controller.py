from app import app
from flask import render_template

@app.route('/ready_pc')
def ready_pc():
    return render_template('main_screen/ready_pc.html')