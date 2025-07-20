from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, IntegerField, FileField, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired
from flask_login import current_user
from app.models.user import User

class ChangeInfo(FlaskForm):
    name = StringField('Введите новое имя' )
    nickname = StringField('Введите новый логин')
    date_of_birth = StringField('Введите новую дату рождения')
    email = EmailField('Введите новую почту' )
    phone_number = StringField('Введите новый номер телефона')
    avatar = FileField('Добавьте новое фото профиля', validators=[FileAllowed(['jpg','png','gif','webp'], 'Можно загружать только картинки!' )])
    submit = SubmitField('Изменить данные')


    def validate_name(form, name):
        if len(name.data) < 2:
            raise ValidationError('Имя не может содержать 1 букву')
        user = User.query.filter_by(name=name.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Пользователь с таким именем уже существует!')
        
    def validate_nickname(form, nickname):
        if len(nickname.data) < 3:
            raise ValidationError('Логин не должен быть короче 3 символов!')
        user_nickname = User.query.filter_by(nickname=nickname.data).first()
        if user_nickname and user_nickname.id != current_user.id:
            raise ValidationError('Пользователь с таким логином уже существует!')
        
    def validate_phone_number(form, phone_number):
        if len(str(phone_number.data)) > 12 or len(str(phone_number.data)) < 11:
            raise ValidationError('Номер должен содержать от 11 до 12 цифр!')
        user_phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if user_phone_number and user_phone_number.id != current_user.id:
            raise ValidationError('Пользователь с таким номером телефона уже сущестует!')
        
    def validate_email(form, email):
        if len(email.data) < 3:
            raise ValidationError('Почта не может содержать менее 3 символов!')
        user_email = User.query.filter_by(email=email.data).first()
        if user_email and user_email.id != current_user.id:
            raise ValidationError('Пользователь с такой почтой уже существует!')        

   
