import importlib


def principal_menu():
    from app.login import(
        admin,
        editor,
        user as u
    )
    permisions = [
        {'inventory': editor},
        {'user': admin}]
    menu = []
    for item in permisions:
        for m, p in item.items():
            if not p.can():
                continue
            module_obj = importlib.import_module('app.modules.' + m)
            menu.append(module_obj.config)
    return menu
