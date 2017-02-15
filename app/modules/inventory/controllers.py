"""Controller of inventory."""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify
from flask_login import login_required

import re
# Import the database object from the main app module
import json

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
        data = json.loads(request.form.get("args"))
        draw = data['draw']
        length = data['length']
        start = data['start']
        search = data['search']['value']
        result = []
        response = {}
        count = 0
        total = Inventory.objects.filter(deleted=False).count()
        if search:
            keys = Inventory._fields.keys()
            keys.remove('id')
            params = [{'deleted': False}]
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
                result = Inventory.objects.filter(deleted=False) \
                                          .limit(length) \
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
    return render_template("inventory/list.html",
                           menu=principal_menu(),
                           config=config,
                           tipo_choices=dict(tipo_choices))


@inventory.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create Method."""
    form = InventoryForm(request.form)
    if form.validate_on_submit():
        obj = Inventory()
        form.populate_obj(obj)
        obj.deleted = False
        Inventory.objects.insert(obj)
        flash("Elemento creado", "success")
        return redirect(url_for("inventory.list"))
    return render_template("inventory/create.html",
                           action="create",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@inventory.route('/edit/<string:key>', methods=['GET', 'POST'])
@login_required
def edit(key):
    """Edit Method."""
    try:
        element = Inventory.objects.filter(deleted=False,
                                           id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("inventory.list"))
    if request.method == 'GET':
        form = InventoryForm(request.form, element)
        return render_template("inventory/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)
    else:
        form = InventoryForm(request.form)
        if form.validate_on_submit():
            element.update(**form.data)
            flash("Elemento Actualizado", "success")
            return redirect(url_for("inventory.list"))
        return render_template("inventory/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)


@inventory.route('/delete/<string:key>', methods=['GET'])
@login_required
def delete(key):
    """Delete Method."""
    try:
        element = Inventory.objects.filter(deleted=False,
                                           id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("inventory.list"))
    element.update(deleted=True)
    flash("Elemento Eliminado", "success")
    return redirect(url_for("inventory.list"))


@inventory.route('/export/<string:type>', methods=['GET'])
@inventory.route('/export/<string:type>/<string:key>', methods=['GET'])
@login_required
def export(type='xls', key=None):
    """Export Method."""
    pass
