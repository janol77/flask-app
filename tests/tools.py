"""Tools."""
from app.modules.user import User
from app.modules.inventory import Inventory
from werkzeug import generate_password_hash
import string
import random


users = [{'name': 'Admin',
          'email': 'admin@admin.cl',
          'password': 'admin',
          'deleted': False},
         {'name': 'Alejandro',
          'email': 'alejandro@alejandro.cl',
          'password': 'alejandro',
          'deleted': False}]

products = [{'optico': 'Oakley',
             'tipo': 'sol',
             'ean': '12345678',
             'deleted': False},
            {'optico': 'Arnette',
             'tipo': 'contacto',
             'ean': '12345678',
             'deleted': False}]


def init_users():
    """Inicializar la base de datos."""
    users_ids = {}
    for user in users:
        users_list = User.objects.filter(email=user['email'])
        user_object = users_list.first()
        if not user_object:
            user['password'] = generate_password_hash(user['password'])
            element = User(**user).save()
            users_ids[user['name']] = str(element.id)
    return users_ids


def remove_users():
    User.objects.delete()


def init_products():
    """Inicializar la base de datos."""
    products_ids = {}
    for product in products:
        product_list = Inventory.objects.filter(optico=product['optico'])
        product_object = product_list.first()
        if not product_object:
            element = Inventory(**product).save()
            products_ids[product['optico']] = str(element.id)
    return products_ids


def remove_products():
    Inventory.objects.delete()


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))