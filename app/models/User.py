from app import db, login_manager
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return db.session.query(User).get(int(usuario_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    cpf = db.Column(db.String(12), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    user_type = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(100))

    # reservation relation
    reservations = relationship("Reservation", back_populates="user")

    def __init__(self, name, email, cpf, password, user_type, phonenumber):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.set_password(password)
        self.user_type = user_type
        self.phonenumber = phonenumber

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.cpf}')"
