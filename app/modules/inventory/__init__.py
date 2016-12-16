from flask import Blueprint


inventory = Blueprint('inventory', __name__)

from . import controllers

config = {}
config['name'] = "Inventario"
config['menu'] = {'Lista': 'inventory.list',
                  'Crear': 'inventory.create'}

def get_config():
    return config
