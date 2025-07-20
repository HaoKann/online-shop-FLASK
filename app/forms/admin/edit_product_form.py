from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

class EditProduct(FlaskForm):
    name = StringField(' Новое имя ', validators=[DataRequired()])
    category = StringField('Новая категорию ', validators=[DataRequired()])
    price = IntegerField('Новая цену ', validators=[DataRequired()])
    discount = IntegerField(' Скидка(необязательно)', default=0)
    submit = SubmitField('Изменить товар')