from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EditProduct(FlaskForm):
    name = StringField(' Новое имя ', validators=[DataRequired()])
    category_id = SelectField('Категория ', coerce=int, validators=[DataRequired()])
    price = IntegerField('Новая цену ', validators=[DataRequired()])
    discount = IntegerField('Скидка(необязательно)', default=0)
    submit = SubmitField('Изменить товар')