from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class AdminEditOrder(FlaskForm):
    phone_number = IntegerField('Номер телефона', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    address = StringField('Адрес доставки', validators=[DataRequired()])
    way_of_delivery = SelectField('Способ доставки', choices=[
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
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменён')
    ])
    submit = SubmitField('Изменить заказ')
