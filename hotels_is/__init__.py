from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import urllib

TESTS = True

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x98N\xa4\x99\xab\x97\x00&\xd4H\xb4V"\n\xe32xB\x9da\x9d\xa6\xfbq\x87[5w\x9b\xbac\x97\x12<\x86\x04\x93\xbb\xee\xebXt^\x96r\xf4`\xb8\x86n'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# config for the filemanager
app.config['IMG_UPLOAD_URL'] = '/static/uploads/'
app.config['IMG_UPLOAD_FOLDER'] = '/static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from hotels_is import routes

from hotels_is.blueprints.create import create
app.register_blueprint(create, url_prefix='/create')

from hotels_is.blueprints.update import update
app.register_blueprint(update, url_prefix='/update')

from hotels_is.blueprints.delete import delete
app.register_blueprint(delete, url_prefix='/delete')

from hotels_is.blueprints.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

from hotels_is.blueprints.recepcni import recepcni
app.register_blueprint(recepcni, url_prefix='/recepcni')

from hotels_is.blueprints.zakaznik import zakaznik
app.register_blueprint(zakaznik, url_prefix='/zakaznik')

from hotels_is.blueprints.everyone import everyone
app.register_blueprint(everyone, url_prefix='/everyone')

from hotels_is.blueprints.vlastnik import vlastnik
app.register_blueprint(vlastnik, url_prefix='/vlastnik')

from hotels_is.blueprints.obrazek import obrazek
app.register_blueprint(obrazek, url_prefix='/obrazek')

if TESTS:
    from hotels_is.tests.database import *
    fill_db_with_reference_data()