
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class AddProduct(FlaskForm):
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
    price = IntegerField('Цена товара', validators=[DataRequired()])
    discount = IntegerField('Скидка(необязательно)', default=0)
    submit = SubmitField('Добавить товар')

class CharacteristicsForm(FlaskForm):
    name = StringField('Название характиристики',validators=[DataRequired()])
    int_value = IntegerField('Числовая характеристика', validators=[DataRequired()], default=0)
    str_value = StringField('Строковая характиристика',validators=[DataRequired()])
    submit_characteristics = SubmitField('Добавить характеристику')

class PhotoForm(FlaskForm):
    photo = FileField('Добавить фото товара: ', validators=[FileAllowed(['jpg','png','gif'], 'Можно загружать только картинки!' )])
    description = StringField('Описание картинки',validators=[DataRequired()])
    submit_photo = SubmitField('Добавить фото')

