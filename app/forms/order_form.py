from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    address = StringField('Введите адрес доставки', validators=[DataRequired()])
    way_of_delivery = SelectField('Выберите способ доставки', choices=[
        ('Курьерская служба', 'Курьерская служба'),
        ('Самовывоз', 'Самовывоз')
    ])
    time_of_arrival = SelectField('Выберите время доставки', choices=[
        ('7:00-11:00', 'Утреннее(7:00-11:00)'),
        ('12:00-18:00', 'Дневное время(12:00-18:00)'),
        ('18:00-00:00', 'Вечернее время(18:00-00:00)')
    ])
    status = SelectField('Статус заказа', choices=[
        ('pending', 'Оформлен'),
        ('shipped', 'В пути'),
        ('delivered', 'Доставлен')
    ])
    submit = SubmitField('Заказать')