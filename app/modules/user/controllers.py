# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  jsonify
from flask_login import login_required

import re
# Import the database object from the main app module


from forms import UserForm

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
        draw = int(request.form.get('draw'))
        length = int(request.form.get('length'))
        start = int(request.form.get('start'))
        search = request.form.get('search[value]')
        result = []
        response = {}
        count = 0
        total = User.objects.count()
        keys = User._fields.keys()
        keys.remove('password')
        fields = keys[:]
        keys.remove('id')
        if search:
            params = []
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
                result = User.objects.only(*fields) \
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
        User.objects.insert(obj)
        return redirect(url_for("user.list"))

    return render_template("user/create.html",
                           form=form,
                           menu=principal_menu(),
                           config=config)
