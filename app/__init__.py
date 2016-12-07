from flask_login import login_required
from db import db
# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CsrfProtect
from login import login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
    app.debug = True
    app.config['DEBUG_TB_PANELS'] = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_mongoengine.panels.MongoDebugPanel'
    )
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # Define the WSGI application object
    db.init_app(app)
    # csrf protection
    csrf = CsrfProtect()
    csrf.init_app(app)
    # Register blueprint(s)
    login_manager.init_app(app)
    from .modules.inventory import inventory as inventory_blueprint
    app.register_blueprint(inventory_blueprint, url_prefix='/inventory')
    from login import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route("/", methods=['GET'])
    @login_required
    def index():
        return redirect(url_for('inventory.home'))

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    return app
