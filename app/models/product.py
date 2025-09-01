from app import db
from flask import url_for

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    discount = db.Column(db.Integer(), default=0)

    # db.ForeignKey - создает связь на стороне 'Много'
    # user_id = db.Column(db.Integer(), db.ForeignKey('users.id')) 
    
    photos = db.relationship('Photo', backref='product', lazy='dynamic', 
                           cascade='all, delete-orphan', passive_deletes=True)
    characteristics = db.relationship('Characteristic', backref='product', lazy='dynamic',
                                    cascade='all, delete-orphan', passive_deletes=True)
    product_in_carts = db.relationship('ProductInCart', backref='product', lazy='dynamic',
                                     cascade='all, delete-orphan', passive_deletes=True)
    favourite_by_users = db.relationship('FavouriteProduct', backref='product', lazy='dynamic',
                                       cascade='all, delete-orphan', passive_deletes=True)
    product_in_ready_pcs = db.relationship('ProductInReadyPC', backref='product', lazy='dynamic',
                                           cascade='all, delete-orphan')

    def get_first_photo(self):
        if self.photos.first():
            return self.photos.first().get_photo()
        else:
            return '/static/img/default.webp'
        
    def get_discount_price(self):
        if self.discount:
            discount_price = self.price * self.discount / 100
            total_price = self.price - discount_price
            return round(total_price)
        else:
            return self.price
        

    def get_category_name(self):
        category_map = {
            'gpu': 'Видеокарта',
            'cpu': 'Процессор',
            'motherboard': 'Материнская плата',
            'ram': 'Оперативная память',
            'psu': 'Блок питания',
            'cooler': 'Система охлаждения',
            'storage': 'Накопитель',
            'pc_case': 'Корпус',
        }
        return category_map.get(self.category, self.category)



class ReadyPC(db.Model):
    __tablename__='readypc'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False, default=0)  
    amount = db.Column(db.Integer(), nullable=False, default=1)

    products_in_readypc = db.relationship('ProductInReadyPC', backref='ready_pc', lazy='dynamic', cascade='all, delete-orphan' )


     # --- НАЧАЛО НОВЫХ МЕТОДОВ ---

    def get_component(self, category_name):
        """Универсальный метод для поиска компонента по категории."""
        for component in self.products_in_readypc:
            if component.product.category == category_name:
                return component.product
        return None

    def get_cpu(self):
        """Возвращает название процессора."""
        cpu_product = self.get_component('cpu')
        return cpu_product.name if cpu_product else 'Не указан'

    def get_gpu(self):
        """Возвращает название видеокарты."""
        gpu_product = self.get_component('gpu')
        return gpu_product.name if gpu_product else 'Не указана'
        
    def get_ram(self):
        """Возвращает название оперативной памяти."""
        ram_product = self.get_component('ram')
        return ram_product.name if ram_product else 'Не указана'
    
    def get_motherboard(self):
        motherboard_product = self.get_component('motherboard')
        return motherboard_product.name if motherboard_product else 'Не указана'
    
    def get_power_supply_unit(self):
        power_supply_unit_product = self.get_component('psu')
        return power_supply_unit_product.name if power_supply_unit_product else 'Не указан'
        
    def get_cooler(self):
        cooler_product = self.get_component('cooler')
        return cooler_product.name if cooler_product else 'Не указан'
    
    def get_storage(self):
        storage_product = self.get_component('storage')
        return storage_product.name if storage_product else 'Не указан'

    def get_pc_case(self):
        get_pc_case = self.get_component('pc_case')
        return get_pc_case.name if get_pc_case else 'Не указан'
        
    def get_cooler(self):
        cooler_product = self.get_component('cooler')
        return cooler_product.name if cooler_product else 'Не указан'

    def get_build_image(self):
        """Возвращает фото корпуса, если он есть, иначе - фото по умолчанию."""
        case_product = self.get_component('pc_case')
        if case_product and case_product.photos.first():
            return case_product.get_first_photo()
        return '/static/img/default_pc.webp' # Убедитесь, что у вас есть такое фото

    # --- КОНЕЦ НОВЫХ МЕТОДОВ ---

    def get_absent_categories(self):
        category_map = {
            'gpu': 'Видеокарта',
            'cpu': 'Процессор',
            'motherboard': 'Материнская плата',
            'ram': 'Оперативная память',
            'psu': 'Блок питания',
            'cooler': 'Система охлаждения',
            'storage': 'Накопитель',
            'pc_case': 'Корпус',
        }

        for component in self.products_in_readypc.all():
            if component.product.category in category_map:
                category_map.pop(component.product.category)
        return category_map
    

    def is_ready(self):
        return len(self.get_absent_categories()) == 0


class ProductInReadyPC(db.Model):
    __tablename__='productsinreadypc'

    id = db.Column(db.Integer(), primary_key=True) 
    amount = db.Column(db.Integer(), nullable=False, default=1)
    ready_pc_id = db.Column(db.Integer(), db.ForeignKey('readypc.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'), nullable=False)



class Characteristic(db.Model):
    __tablename__ = 'characteristics'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    int_value = db.Column(db.Integer(), nullable=False)
    str_value = db.Column(db.String(30), nullable=False)
    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)
    photo_path = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    prod_id = db.Column(db.Integer(), db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)

    def get_photo(self):
        return url_for('static', filename=f'products_photo/{self.product.category}/{self.product.id}/{self.photo_path}')
    
