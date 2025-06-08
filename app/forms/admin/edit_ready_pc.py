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


    # Этот метод запускается, когда создаётся форма. Он заполняет выпадающие списки товарами из базы
    def __init__(self, ready_pc=None, *args, **kwargs):
        # Вызывает конструктор родительского класса FlaskForm, 
        # чтобы настроить базовую функциональность формы (например, обработку CSRF-токена или валидации)
        super(EditReadyPC, self).__init__(*args, **kwargs)
        # Сохраняет переданный объект сборки (ready_pc) как атрибут формы.
        #  Это нужно, чтобы потом использовать его для предзаполнения полей.
        self.ready_pc = ready_pc

        # Получаем все доступные продукты по категориям
        categories = ['cpu','gpu','motherboard','ram','psu','cooler','storage','pc_case']

        # Использует список categories для запроса всех продуктов из базы данных по каждой категории.
        #  Результат сохраняется в словаре all_products, 
        # где ключ — категория (например, cpu), а значение — список продуктов (например, все процессоры).
        all_products = {cat: Product.query.filter_by(category=cat).all() for cat in categories}

        # Заполняем choices для каждого поля
        
        for cat in categories:
            # Создаёт список пар (ID, название) для каждого продукта в данной категории.
            choices = [(str(p.id), p.name) for p in all_products[cat] ]
            # Присваивает сформированный список choices полю формы, соответствующему текущей категории.
            # getattr(obj, name) — это функция, которая динамически получает атрибут объекта по его имени (в виде строки). 
            # Здесь self — это форма, а cat — имя поля (например, 'cpu'). 
            # Вместо self.cpu.choices = choices пишем getattr(self, cat).choices = choices, чтобы работать с полем по его имени из списка.
            getattr(self, cat).choices = choices

        # Если редактируется существующая сборка (ready_pc не None), 
        # проверяем текущие комплектующие и устанавливаем их значения в соответствующие поля.
        if ready_pc:
            for component in ready_pc.products_in_readypc.all():
                cat = component.product.category
                # Проверяет, есть ли в форме поле с именем cat (например, cpu).
                #  Функция hasattr(obj, name) возвращает True, если атрибут существует.
                if hasattr(self, cat):
                    getattr(self, cat).data = str(component.product_id)