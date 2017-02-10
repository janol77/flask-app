# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module


from forms import UserForm

# Import module models (i.e. User)
from models import User

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import user, config
from app.modules import principal_menu


# Set the route and accepted methods
@user.route('/list', methods=['GET'])
@login_required
def list():
    form = UserForm(request.form)
    return render_template("user/list.html",
                           form=form,
                           menu=principal_menu(),
                           config=config)


# Set the route and accepted methods
@user.route('/create', methods=['GET'])
@login_required
def create():
    form = UserForm(request.form)
    return render_template("user/create.html",
                           form=form,
                           menu=principal_menu(),
                           config=config)
