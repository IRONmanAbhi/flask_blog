from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "8389a9cec477d2ab55aa06fc0fbcc96c"
basedir = os.path.abspath(os.path.dirname(__file__))  # Get the directory where __init__.py is located
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "site.db")
# this should be kept as an environment variable
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


from flaskblog import routes