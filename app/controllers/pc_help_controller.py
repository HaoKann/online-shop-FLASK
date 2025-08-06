from flask import render_template, Blueprint
from flask_login import login_required

# 1. Имя блюпринта - это просто строка 'pc_help'
pc_help_bp = Blueprint('pc_help', __name__)

@pc_help_bp.route('/pc_help')
@login_required
def pc_help():
    return render_template('main_screen/pc_help.html')