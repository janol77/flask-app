# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify
from flask_login import login_required

import re
# Import the database object from the main app module
import json

from forms import UserForm, EditUserForm

# Import module models (i.e. User)
from models import User

# Define the blueprint: 'auth', set its url prefix: url/auth
from . import user, config
from app.modules import principal_menu


# Set the route and accepted methods
@user.route('/', methods=['GET'])
@user.route('/list', methods=['GET', 'POST'])
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
        total = User.objects.filter(deleted=False).count()
        keys = User._fields.keys()
        keys.remove('password')
        fields = keys[:]
        keys.remove('id')
        if search:
            params = [{'deleted': False}]
            regex = re.compile('.*%s.*' % search)
            for key in keys:
                params.append({key: regex})
            try:
                result = User.objects.filter(__raw__={"$or": params}) \
                                     .only(*fields) \
                                     .limit(length) \
                                     .skip(start)
                count = User.objects.filter(__raw__={"$or": params}) \
                                    .count()
            except Exception as e:
                print e
        else:
            try:
                result = User.objects.filter(deleted=False) \
                                     .only(*fields) \
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
    return render_template("user/list.html",
                           menu=principal_menu(),
                           config=config)


# Set the route and accepted methods
@user.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create Method."""
    form = UserForm(request.form)
    if form.validate_on_submit():
        obj = User()
        form.populate_obj(obj)
        obj.generate_password()
        obj.deleted = False
        User.objects.insert(obj)
        flash("Usuario creado", "success")
        return redirect(url_for("user.list"))
    return render_template("user/create.html",
                           action="create",
                           form=form,
                           menu=principal_menu(),
                           config=config)


@user.route('/edit/<string:key>', methods=['GET', 'POST'])
@login_required
def edit(key):
    """Edit Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    if request.method == 'GET':
        form = EditUserForm(request.form, element)
        return render_template("user/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)
    else:
        form = EditUserForm(request.form)
        if not element.check_email(form.email.data):
            form.exist_mail()
            flash("Email ya utilizado", "error")
        elif form.validate_on_submit():
            form.populate_obj(element)
            element.generate_password()
            element.save()
            flash("Elemento Actualizado", "success")
            return redirect(url_for("user.list"))
        return render_template("user/create.html",
                               action="edit",
                               form=form,
                               menu=principal_menu(),
                               config=config)


@user.route('/delete/<string:key>', methods=['GET'])
@login_required
def delete(key):
    """Delete Method."""
    try:
        element = User.objects.filter(deleted=False,
                                      id=key).first()
    except Exception:
        flash("Elemento No encontrado", "error")
        return redirect(url_for("user.list"))
    element.update(deleted=True)
    flash("Elemento Eliminado", "success")
    return redirect(url_for("user.list"))
