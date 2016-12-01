import datetime
from flask_login import login_required
from db import db
# Import flask and template operators
from flask import Flask, render_template, redirect, url_for, request


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

from app.inventory.controllers import init_app as inventory_module
from login import init_app as auth_module

# Register blueprint(s)
inventory_module(app)
auth_module(app)

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    return redirect(url_for('inventory.home'))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
