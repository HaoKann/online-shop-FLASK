from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    address = StringField('Введите адрес доставки', validators=[DataRequired()])
    way_of_delivery = SelectField('Выберите способ доставки', choices=[
        ('courier', 'Курьерская служба'),
        ('self-delivery', 'Самовывоз')
    ])
    time_of_arrival = SelectField('Выберите время доставки', choices=[
        ('morning', 'Утреннее(7:00-11:00)'),
        ('day', 'Дневное время(12:00-18:00)'),
        ('evening', 'Вечернее время(18:00-00:00)')
    ])
    submit = SubmitField('Заказать')