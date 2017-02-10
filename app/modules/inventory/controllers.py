"""Controller of inventory."""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify
from flask_login import login_required
from mongoengine.queryset.visitor import Q

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash
import re
# Import the database object from the main app module


from forms import InventoryForm, tipo_choices

# Import module models (i.e. User)
from models import Inventory

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import inventory, config
# from inventory import principal_menu
from app.modules import principal_menu


@inventory.route('/', methods=['GET'])
@inventory.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    """List Method."""
    if request.method == 'POST':
        draw = int(request.form.get('draw'))
        length = int(request.form.get('length'))
        start = int(request.form.get('start'))
        search = request.form.get('search[value]')
        result = []
        response = {}
        count = 0
        total = Inventory.objects.count()
        if search:
            keys = Inventory._fields.keys()
            keys.remove('id')
            params = []
            regex = re.compile('.*%s.*' % search)
            for key in keys:
                params.append({key: regex})
            try:
                result = Inventory.objects.filter(__raw__={"$or": params}) \
                                          .limit(length) \
                                          .skip(start)
                count = Inventory.objects.filter(__raw__={"$or": params}) \
                                         .count()
            except Exception as e:
                print e
        else:
            try:
                result = Inventory.objects.limit(length) \
                                          .skip(start)
                count = total
            except Exception as e:
                print e

        # order = int(request.form.get('order[0][column]'))
        # order_dir = request.form.get('order[0][dir]')
        response['draw'] = draw
        response["recordsTotal"] = total
        response["recordsFiltered"] = count
        response["data"] = result
        return jsonify(response)
    elements = Inventory.objects.all()
    form = InventoryForm(request.form)
    return render_template("inventory/list.html",
                           form=form,
                           menu=principal_menu(),
                           config=config,
                           elements=elements,
                           tipo_choices=dict(tipo_choices))


@inventory.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create Method."""
    form = InventoryForm(request.form)
    if form.validate_on_submit():
        obj = Inventory()
        form.populate_obj(obj)
        Inventory.objects.insert(obj)
        return redirect(url_for("inventory.list"))

    return render_template("inventory/create.html",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@inventory.route('/edit/<string:key>', methods=['GET'])
@login_required
def edit(key=None):
    """Edit Method."""
    pass


@inventory.route('/delete/<string:key>', methods=['GET'])
@login_required
def delete(key=None):
    """Delete Method."""
    pass


@inventory.route('/export/<string:type>', methods=['GET'])
@inventory.route('/export/<string:type>/<string:key>', methods=['GET'])
@login_required
def export(type='xls', key=None):
    """Export Method."""
    pass
