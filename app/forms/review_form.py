from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length

class UserReviewForm(FlaskForm):
    rating = IntegerField(
        'Ваша оценка (1-5)',
        validators=[
            DataRequired(message='Оценка обязательна'),
            NumberRange(min=1, max=5, message='Оценка должна быть от 1 до 5')
        ]
    )

    # Текст отзыва
    text = TextAreaField(
        'Текст отзыва',
        validators=[
            DataRequired(message='Текст отзыва обязателен'),
            Length(min=10, max=500, message='Отзыв должен содержать от 10 до 500 символов')
        ],
        render_kw={'rows': 4, 'placeholder': 'Поделиться своим мнение о продукте...'}
    )

    # Скрытое поле для ID продукта (Обязательно для передачи контекста)
    product_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Отправить отзыв')