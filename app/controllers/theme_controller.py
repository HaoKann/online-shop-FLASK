from flask import redirect, request, g, make_response, Blueprint


theme_bp = Blueprint('theme', __name__)


@theme_bp.route('/toggle_theme')
def toggle_theme():
    current_theme = request.cookies.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'

    response = make_response(redirect(request.referrer or '/'))
    response.set_cookie('theme', new_theme, max_age=30*24*60*60)
    return response
    