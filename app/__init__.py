from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from itsdangerous import URLSafeSerializer

db = SQLAlchemy()
login_manager = LoginManager()
serializer = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    global serializer
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.controllers import register_blueprints
        register_blueprints(app)
        db.create_all()

    return app

