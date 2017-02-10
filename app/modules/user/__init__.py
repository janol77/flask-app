from flask import Blueprint

user = Blueprint('user', __name__)
config = {}
config['name'] = "Usuarios"
config['menu'] = {'Lista': 'user.list',
                  'Crear': 'user.create'}

from controllers import *


def get_config():
	return config
