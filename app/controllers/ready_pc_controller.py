from app import db
from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import current_user
from app.models.product import ReadyPC
from app.forms.empty_form import EmptyForm
from app.models.review import Review
from app.forms.review_form import UserReviewForm

ready_pc_bp = Blueprint('ready_pc', __name__)

@ready_pc_bp.route('/ready_pc')
def ready_pc():
    # 1. Получаем номер страницы из URL (например, /ready_pc?page=2).
    #    Если номер не указан, по умолчанию будет 1.
    page = request.args.get('page', 1, type=int)
    #  2. Вместо .all() используем .paginate().
    query = ReadyPC.query
    current_sort = request.args.get('sort', 'newest')

    if current_sort == 'price_asc':
        query = query.order_by(ReadyPC.price.asc())
    elif current_sort == 'price_desc':
        query = query.order_by(ReadyPC.price.desc())
    else:
        query = query.order_by(ReadyPC.id.desc())

    all_ready_pc = query.paginate(page=page, per_page=9, error_out=False)

    csrf_form = EmptyForm()

    return render_template('main_screen/ready_pc.html', all_ready_pc=all_ready_pc, csrf_form=csrf_form, current_sort=current_sort)


@ready_pc_bp.route('/ready_pc/<int:build_id>', methods=['GET','POST'])
def ready_pc_details(build_id):
    # Находим сборку по ID, если не найдена - выдаем ошибку 404
    ready_pc = ReadyPC.query.get_or_404(build_id)

    # Используем форму отзывов вместо EmptyForm
    form = UserReviewForm()

    if request.method == 'POST':
        rating_val = request.form.get('rating')


    if form.text.data and rating_val:
        new_review = Review(
            text = form.text.data,
            rating = int(rating_val),
            user_id = current_user.id,
            ready_pc_id = ready_pc.id,
            is_approved = False # Отправляем на модерацию
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Спасибо! Ваш отзыв отправлен на модерацию', 'success')
        return redirect(url_for('ready_pc.ready_pc_details', build_id=build_id))
    else:
        if not rating_val:
            flash('Пожалуйста, выберите оценку (звезды)', 'danger')
        if not form.text.data:
            flash('Напишите текст отзыва','danger')
    
    # Получаем только одобренные отзывы для этой сборки
    approved_reviews = ready_pc.reviews.filter_by(is_approved=True).order_by(Review.date_posted.desc()).all()

    return render_template('main_screen/ready_pc_details.html', 
                           ready_pc=ready_pc, 
                           form=form,
                           approved_reviews=approved_reviews, 
                           average_rating=ready_pc.average_rating or 0, 
                           reviews_count=ready_pc.reviews_count or 0)