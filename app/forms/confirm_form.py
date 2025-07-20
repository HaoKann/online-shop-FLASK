from flask_wtf import FlaskForm 
from wtforms import SubmitField


class ConfirmForm(FlaskForm):
    confirm = SubmitField('Подтвердить')