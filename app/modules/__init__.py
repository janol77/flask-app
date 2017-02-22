import importlib

modules = ['inventory', 'user']


def principal_menu():
    menu = []
    for m in modules:
        module_obj = importlib.import_module('app.modules.' + m)
        menu.append(module_obj.config)
    return menu
