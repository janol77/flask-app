from flask import Blueprint


inventory = Blueprint('inventory', __name__)
config = {}
config['name'] = "Inventario"
config['menu'] = {'list': {'link': 'inventory.list', 'name': 'Lista'},
                  'create': {'link': 'inventory.create', 'name': 'Crear'}}

from controllers import *


def get_config():
    return config
