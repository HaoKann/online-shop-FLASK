from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app.models.product import Product, Category

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
        
        # Список системных имен (slug) категорий
        categories_slugs = ['cpu','gpu','motherboard','ram','psu','cooler','storage','pc_case']

        for cat_slug in categories_slugs:
            # 1. Формируем запрос с явным соединением таблиц
            products_in_category = Product.query.join(Category).filter(
                # 2. Фильтруем по полю 'slug' в таблице 'Category'
                Category.slug == cat_slug
            ).all()

            # 3. Находим соответствующее поле формы (например, self.cpu)
            field = getattr(self, cat_slug)

            # Заполняем его варианты выбора всеми продуктами из нужной категории
            field.choices = [(str(p.id), p.name) for p in products_in_category]