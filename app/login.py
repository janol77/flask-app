# -*- coding: utf-8 -*-
from app.modules.user.forms import LoginForm

from app.modules.user.models import User

from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import LoginManager, login_user, logout_user, login_required

from werkzeug import check_password_hash

login_manager = LoginManager()
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    "New class."
    user = User.objects.filter(id=user_id).first()
    return user


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    errors = {}
    form = LoginForm()
    if form.validate_on_submit():
        users = User.objects.filter(email=form.email.data)
        user = users.first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("logeado Correctamente", "success")
            return redirect(url_for("index"))
        flash("Credenciales invalidas", "error")

    return render_template("auth/login.html", form=form)
