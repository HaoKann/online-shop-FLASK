from app import app, db
from flask import redirect, render_template, url_for, flash, request
from flask_login import login_required, current_user, logout_user, login_user
from app.forms.user.reg_form import RegForm
from app.forms.user.login_form import LoginForm
from app.models.user import User
from app.models.cart import Cart
from urllib.parse import urlparse

@app.route('/reg', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    form = RegForm()


    if form.validate_on_submit():
        registered_user = User(name=form.name.data, 
                               nickname=form.nickname.data, 
                               date_of_birth=form.date_of_birth.data, 
                               email=form.email.data, 
                               phone_number=form.phone_number.data)
        registered_user.set_password(form.new_password.data)
        db.session.add(registered_user)
        db.session.commit()
        cart = Cart(user_id=registered_user.id)
        db.session.add(cart)
        db.session.commit()
        flash('Аккаунт успешно создан!', 'success')
        return redirect(url_for('login'))
    return render_template('auth/registration.html', form=form, sub_title='Регистрация')

@app.route('/login', methods=['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.new_password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main')
            flash('Вы вошли в аккаунт!', 'success')
            if not user.cart:
                cart = Cart(user_id=user.id)
                db.session.add(cart)
                db.session.commit()
            return redirect(next_page)
        flash('Неверный логин или пароль', 'danger')
        return redirect(url_for('login'))
    return render_template('auth/login.html', form=form, sub_title='Авторизация')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'info')
    return redirect(url_for('login'))
