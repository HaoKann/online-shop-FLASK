from flask import render_template, Blueprint
from flask_login import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
@login_required
def user():
    return render_template('user/userpage.html')