from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from app.models.product import Product

class EditReadyPC(FlaskForm):
    name = StringField('Название сборки', validators=[DataRequired()])

    gpu = SelectField('Видеокарта', validators=[DataRequired()])
    cpu = SelectField('Процессор', validators=[DataRequired()])
    motherboard = SelectField('Материнская плата', validators=[DataRequired()])
    psu = SelectField('Блок питания', validators=[DataRequired()])
    ram = SelectField('ОЗУ', validators=[DataRequired()])
    cooler = SelectField('Система охлаждения', validators=[DataRequired()])
    storage = SelectField('Накопитель', validators=[DataRequired()])
    pc_case = SelectField('Корпус', validators=[DataRequired()])

    submit = SubmitField('Обновить сборку')

    def __init__(self, ready_pc=None, *args, **kwargs):
        super(EditReadyPC, self).__init__(*args, **kwargs)
        self.ready_pc = ready_pc

        # Получаем все доступные продукты по категориям
        categories = ['cpu','gpu','motherboard','ram','psu','cooler','storage','pc_case']

        all_products = {cat: Product.query.filter_by(category=cat).all() for cat in categories}

        # Заполняем choices для каждого поля
        for cat in categories:
            choices = [(str(p.id), p.name) for p in all_products[cat] ]
            getattr(self, cat).choices = choices

        # Если есть текущая сборка, предзаполняем форму текущими значениями 
        if ready_pc:
            for component in ready_pc.products_in_readypc.all():
                cat = component.product.category
                if hasattr(self, cat):
                    getattr(self, cat).data = str(component.product_id)