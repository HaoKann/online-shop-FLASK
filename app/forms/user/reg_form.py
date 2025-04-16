from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models.user import User

class RegForm(FlaskForm):
    name = StringField('Введите имя пользователя', validators=[DataRequired()])
    nickname = StringField('Введите логин', validators=[DataRequired()])
    date_of_birth = DateField('Введите дату рождения', validators=[DataRequired()])
    email = EmailField('Введите почту', validators=[DataRequired()])
    phone_number = StringField ('Введите номер телефона', validators=[DataRequired()])
    new_password = PasswordField('Введите пароль', validators=[DataRequired()])
    check_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_name(form, name):
        if len(name.data) < 2:
            raise ValidationError('Имя не может содержать 1 букву')
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('Пользователь с таким именем уже существует!')
        
    def validate_new_password(form, new_password):
        if len(new_password.data) < 8:
            raise ValidationError('Пароль должен состоять минимум из 8 символов!')
        
    def validate_nickname(form, nickname):
        if len(nickname.data) < 3:
            raise ValidationError('Логин не должен быть короче 3 символов!')
        user_nickname = User.query.filter_by(nickname=nickname.data).first()
        if user_nickname:
            raise ValidationError('Пользователь с таким логином уже существует!')
        
    def validate_phone_number(form, phone_number):
        if len(str(phone_number.data)) > 12 or len(str(phone_number.data)) < 11:
            raise ValidationError('Номер должен содержать от 11 до 12 цифр!')
        user_phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if user_phone_number:
            raise ValidationError('Пользователь с таким номером телефона уже сущестует!')
        
    def validate_email(form, email):
        if len(email.data) < 3:
            raise ValidationError('Почта не может содержать менее 3 символов!')
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('Пользователь с такой почтой уже существует!')        

   
