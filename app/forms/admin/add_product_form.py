
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

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
    value = StringField('Значение', validators=[DataRequired()])
    value_type = SelectField('Тип значения', choices=[('string','Текст'),('integer','Число')], validators=[DataRequired()]) 
    submit_characteristics = SubmitField('Добавить характеристику')

class CategoryCharacteristicForm(FlaskForm):
    name = StringField('Название характеристики', validators=[DataRequired()])
    value_type = SelectField('Тип значения',choices=[('string', 'Текст'),('integer', 'Число')], validators=[DataRequired()])
    submit = SubmitField('Добавить в шаблон')

class PhotoForm(FlaskForm):
    photo = FileField('Добавить фото товара: ', validators=[FileAllowed(['jpg','png','gif'], 'Можно загружать только картинки!' )])
    description = StringField('Описание картинки',validators=[DataRequired()])
    submit_photo = SubmitField('Добавить фото')

