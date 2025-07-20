from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nickname = StringField('Введите логин', validators=[DataRequired()])
    new_password = PasswordField('Введите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти в аккаунт')