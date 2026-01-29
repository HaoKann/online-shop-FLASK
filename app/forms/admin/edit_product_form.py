from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class EditProduct(FlaskForm):
    name = StringField(' Новое имя ', validators=[DataRequired()])
    category_id = SelectField('Категория ', coerce=int, validators=[DataRequired()])
    price = IntegerField('Новая цену ', validators=[DataRequired()])
    discount = IntegerField('Скидка(необязательно)', default=0)
    photo = FileField('Заменить фото товара: ', validators=[FileAllowed(['jpg','png','gif', 'jpeg'], 'Можно загружать только картинки!' )])
    description = StringField('Описание картинки',validators=[DataRequired()])
    submit_photo = SubmitField('Добавить фото')
    submit = SubmitField('Изменить товар')