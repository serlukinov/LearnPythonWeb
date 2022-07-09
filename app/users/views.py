import os
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from app.db import db
from app.users.forms import LoginForm, RegistrationForm

from app.users.models import User
# from app.utils import get_redirect_target
from app.users.models import User
from werkzeug.utils import secure_filename

blueprint = Blueprint('users', __name__, url_prefix='/')


@blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("lessons.index"))
    return redirect(url_for("users.login"))


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("lessons.index"))  # redirect(get_redirect_target())
    title = "Авторизация"
    login_form = LoginForm()
    return render_template("users/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST", "GET"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли на сайт")
            return redirect(url_for("lessons.index"))  # redirect(get_redirect_target())
        else:
            return redirect(url_for("users.register"))
    flash("Неправильные имя пользователя или пароль")
    return redirect(url_for("users.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("users.login"))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('lessons.index'))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template('users/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['GET','POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        f = form.avatar.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            os.path.dirname('config.py'), '..', 'static', 'avatars', filename
        ))
        news_user = User(
            username=form.username.data, 
            email=form.email.data, 
            role='user',
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            # avatar=os.path.dirname(filename),
            )
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return  render_template('welcome_page.html')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('users.register'))


@blueprint.route("/promo")
def promo():
    return render_template('welcome_page.html')