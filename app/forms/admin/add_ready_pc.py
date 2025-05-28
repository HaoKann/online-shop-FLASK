from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ReadyPCForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    category = SelectField(
        'Категория товара',
        choices=[
            ('gpu', 'Видеокарта'),
            ('cpu', 'Процессор'),
            ('motherboard', 'Материнская плата'),
            ('ram', 'Оперативная память'),
            ('psu', 'Блок питания'),
            ('cooler', 'Система охлаждения'),
            ('storage', 'Накопитель'),
            ('pc_case', 'Корпус'),
        ],
        validators=[DataRequired()]
    )
    amount = IntegerField('Количество продукта', validators=[DataRequired()])
    submit = SubmitField('Добавить готовую сборку')