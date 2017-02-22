from flask_login import login_required
from db import db
from login import login_manager

import os
# Import flask and template operators
from flask import Flask, render_template
from flask_wtf.csrf import CsrfProtect
from modules import principal_menu


def create_app(config="config.ini"):
    app = Flask(__name__, static_url_path='/static')
    app.config.update(
        MONGODB_SETTINGS={'DB': 'testapp'},
        TESTING=True,
        SECRET_KEY='flask+mongoengine=<3'
    )
    # Define the WSGI application object
    db.init_app(app)
    # csrf protection
    csrf = CsrfProtect()
    csrf.init_app(app)
    # Register blueprint(s)
    login_manager.init_app(app)
    from modules.inventory import inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    from modules.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from login import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route("/", methods=['GET'])
    @login_required
    def index():
        return render_template("index.html",
                               menu=principal_menu())

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', False)
            )
