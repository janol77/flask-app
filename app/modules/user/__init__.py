from flask import Blueprint


user = Blueprint('user', __name__)

from . import controllers

config = {}
config['name'] = "Usuarios"
config['menu'] = {'Lista': 'user.list',
                  'Crear': 'user.create'}

def get_config():
	return config
