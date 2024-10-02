from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from datetime import timedelta
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv() 

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=60)
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_PORT"] = os.getenv('MAIL_PORT')
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USER')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
# this should be kept as an environment variable
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
mail = Mail(app)

from flaskblog import routes