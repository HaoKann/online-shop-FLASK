from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class FAQForm(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    answer = TextAreaField('Ответ', validators=[DataRequired()])
    category = StringField('Категория (напр. "Доставка", "Оплата")', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    