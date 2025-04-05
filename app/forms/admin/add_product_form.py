
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

class AddProduct(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    category = StringField('Категория товара', validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    discount = IntegerField('Скидка(необязательно)', default=0)
    submit = SubmitField('Добавить товар')



