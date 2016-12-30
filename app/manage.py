from flask_script import Manager
from werkzeug import generate_password_hash
from app.db import db
from flask import Flask
from app.modules.user.models import User
import os


def create_app(config="config.ini"):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(__name__)
    if os.path.exists(config):
        app.config.from_pyfile(config)
    else:
        print("The app does not have a config.ini file")
    # Define the WSGI application object
    db.init_app(app)
    return app

app = create_app()
manager = Manager(app)


@manager.command
def init_db():
    """Inicializar la base de datos."""

    password = generate_password_hash('admin')
    email = "admin@admin.cl"
    name = "Administrador"
    users = User.objects.filter(email=email)
    user = users.first()
    if not user:
        User(email=email, name=name, password=password).save()
    else:
        print "Usuario Administrador creado anteriormente."



if __name__ == "__main__":
    manager.run()
