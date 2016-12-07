from flask import Blueprint


inventory = Blueprint('inventory', __name__)

from . import controllers

config = {}
config['name'] = "Inventario"

def get_config():
	return config