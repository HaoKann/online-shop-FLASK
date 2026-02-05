from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField 

class AddPhotoForm(FlaskForm):
    photo = FileField('Доп. фото', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Только изображения!')
    ])
    submit = SubmitField('Загрузить')