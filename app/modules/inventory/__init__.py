from flask import Blueprint


inventory = Blueprint('inventory', __name__)
config = {}
config['name'] = "Inventario"
config['menu'] = {'Lista': 'inventory.list',
                  'Crear': 'inventory.create'}

from controllers import *


def get_config():
    return config
