# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module


from forms import InventoryForm

# Import module models (i.e. User)
from models import Inventory

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import inventory
# from inventory import principal_menu
from app.modules import principal_menu

# Set the route and accepted methods
@inventory.route('/list', methods=['GET'])
@login_required
def list():
    form = InventoryForm(request.form)
    return render_template("inventory/list.html",
                           form=form,
                           menu=principal_menu())

# Set the route and accepted methods
@inventory.route('/create', methods=['GET'])
@login_required
def create():
    form = InventoryForm(request.form)
    return render_template("inventory/create.html",
                           form=form,
                           menu=principal_menu())