from app import app
from flask import render_template
from app.models.product import ReadyPC

@app.route('/ready_pc')
def ready_pc():
    all_ready_pc = ReadyPC.query.all()
    return render_template('main_screen/ready_pc.html', all_ready_pc=all_ready_pc)