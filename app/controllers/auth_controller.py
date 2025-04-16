from app import app, db
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from app.forms.user.reg_form import RegForm
from app.models.user import User

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
        flash('Аккаунт успешно создан!', 'success')
        return redirect(url_for('main'))
    return render_template('auth/registration.html', form=form)