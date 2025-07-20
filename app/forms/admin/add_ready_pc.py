from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ReadyPCForm(FlaskForm):
    name = StringField('Название сборки', validators=[DataRequired()])
    category = SelectField(
        'Категория сборки',
        choices=[
            ('gaming', 'Игровая'),
            ('office', 'Офисная'),
            ('professional', 'Профессиональная'),
        ],
        validators=[DataRequired()]
    )
    price = IntegerField('Цена сборки', validators=[DataRequired()])
    submit = SubmitField('Добавить готовую сборку')