# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

from app.inventory.forms import InventoryForm

# Import module models (i.e. User)
from app.inventory.models import Inventory

# Define the blueprint: 'auth', set its url prefix: app.url/auth
from . import inventory

# Set the route and accepted methods
@inventory.route('/home/', methods=['GET', 'POST'])
@login_required
def home():
    print 'home'
    form = InventoryForm(request.form)
    return render_template("inventory/index.html", form=form)
