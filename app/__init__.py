from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "username@gmail.com"
app.config['MAIL_PASSWORD'] = "password"
mail = Mail(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
password = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "loginpage"
login_manager.login_message = "You are mot authorised to access this page. Please login first."
login_manager.login_message_category = "danger" 

from app import routes