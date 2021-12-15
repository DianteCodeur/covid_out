from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#jinja_env = Environment(extensions=['jinja2.ext.i18n'])

app.config['SECRET_KEY'] = 'any secret string'


csrf = CSRFProtect()
csrf.init_app(app)    

login = LoginManager(app)
login.login_view = 'login'

login.login_message = "Connectez-vous pour accéder à cette page"

from routes import *
from adminroutes import *
from models import *

