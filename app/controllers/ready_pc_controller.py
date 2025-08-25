
from flask import render_template, request, Blueprint
from app.models.product import ReadyPC

ready_pc_bp = Blueprint('ready_pc', __name__)

@ready_pc_bp.route('/ready_pc')
def ready_pc():
    # 1. Получаем номер страницы из URL (например, /ready_pc?page=2).
    #    Если номер не указан, по умолчанию будет 1.
    page = request.args.get('page', 1, type=int)
    #  2. Вместо .all() используем .paginate().
    all_ready_pc = ReadyPC.query.order_by(ReadyPC.price.asc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('main_screen/ready_pc.html', all_ready_pc=all_ready_pc)


@ready_pc_bp.route('/ready_pc/<int:build_id>')
def ready_pc_details(build_id):
    # Находим сборку по ID, если не найдена - выдаем ошибку 404
    ready_pc = ReadyPC.query.get_or_404(build_id)

    return render_template('main_screen/ready_pc_details.html', ready_pc=ready_pc)