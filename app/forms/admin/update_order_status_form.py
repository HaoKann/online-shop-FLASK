from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class UpdateOrderStatusForm(FlaskForm):
    status = SelectField(
        'Новый статус', 
        choices=[
            ('pending', 'Обрабатывается'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
            ('canceled', 'Отменен')
        ], 
        validators=[DataRequired()]
    )
    submit = SubmitField('Обновить статус')