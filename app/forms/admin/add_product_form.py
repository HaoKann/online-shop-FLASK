
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class AddProduct(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    discount = IntegerField('Скидка(необязательно)', default=0)
    photo = FileField('Добавить фото товара: ', validators=[FileAllowed(['jpg','png','gif', 'jpeg'], 'Можно загружать только картинки!' )])
    description = StringField('Описание картинки',validators=[DataRequired()])
    submit_photo = SubmitField('Добавить фото')
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



