# -*- coding: utf-8 -*-
from flask_login import LoginManager, login_required, login_user, logout_user
from flask import Flask, Blueprint, render_template, redirect, url_for, request
from werkzeug import check_password_hash, generate_password_hash
from app.user.models import User
from app.user.forms import LoginForm

login_manager = LoginManager()
auth = Blueprint('auth', __name__, url_prefix='/auth')

def init_app(app):
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app

@login_manager.user_loader
def load_user(user_id):
    user = User.objects.filter(id=user_id).first()
    return user

@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    print "try to login"
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.filter(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("index"))
    return render_template("auth/signin.html", form=form)