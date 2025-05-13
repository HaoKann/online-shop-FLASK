from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class ChangeTheme(FlaskForm):
    choose_theme = SelectField('Выберите тему', choices=[
        ('light','Светлая тема'),
        ('dark','Темная тема')
    ])
    submit = SubmitField('Применить тему')