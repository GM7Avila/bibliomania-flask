from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Defina sua chave secreta aqui

app.permanent_session_lifetime = timedelta(minutes=5)

# SQL ALCHEMY CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bibliomania'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)