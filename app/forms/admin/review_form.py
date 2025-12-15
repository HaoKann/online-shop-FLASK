from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# Форма для управления отзывами в админке
class ReviewForm(FlaskForm):
    # Поля, которые видит администратор
    rating = IntegerField(
        'Оценка (1-5)',
        validators=[DataRequired(), NumberRange(min=1, max=5, message='Оценка должна быть от 1 до 5')],
        render_kw={'placeholder': 'Введите число от 1 до 5'}
    )
    text = TextAreaField(
        'Текст отзыва',
        validators=[DataRequired()],
        render_kw={'rows': 5, 'placeholder': 'Полный текст отзыва'}
    )
    # Поле для модерации
    is_approved = BooleanField('Одобрить и опубликовать')
    # Скрытое поле для ID продукта, если мы редактируем
    product_id = HiddenField()

    submit = SubmitField('Сохранить отзыв')

class ConfirmForm(FlaskForm):
    submit = SubmitField('Подтвердить')

    
