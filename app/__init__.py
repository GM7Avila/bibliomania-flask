from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(minutes=60)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# SQL ALCHEMY CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bibliomania'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)