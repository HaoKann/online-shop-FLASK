from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app.models.product import Product

class EditReadyPC(FlaskForm):
    name = StringField('Название сборки', validators=[DataRequired()])
    price = IntegerField('Цена сборки', validators=[DataRequired()])
    
    # Поля для комплектующих
    gpu = SelectField('Видеокарта', validators=[DataRequired()])
    cpu = SelectField('Процессор', validators=[DataRequired()])
    motherboard = SelectField('Материнская плата', validators=[DataRequired()])
    psu = SelectField('Блок питания', validators=[DataRequired()])
    ram = SelectField('Оперативная память', validators=[DataRequired()])
    cooler = SelectField('Система охлаждения', validators=[DataRequired()])
    storage = SelectField('Накопитель', validators=[DataRequired()])
    pc_case = SelectField('Корпус', validators=[DataRequired()])
    
    submit = SubmitField('Обновить сборку')

    # Конструктор теперь ТОЛЬКО заполняет варианты выбора
    def __init__(self, *args, **kwargs):
        super(EditReadyPC, self).__init__(*args, **kwargs)
        
        categories = ['cpu','gpu','motherboard','ram','psu','cooler','storage','pc_case']
        for cat in categories:
            # Динамически получаем поле формы по имени (например, self.cpu)
            field = getattr(self, cat)
            # Заполняем его варианты выбора всеми продуктами из нужной категории
            field.choices = [(str(p.id), p.name) for p in Product.query.filter_by(category=cat).all()]