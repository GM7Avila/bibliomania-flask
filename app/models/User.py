from app import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(120), nullable=False)
    email = db.Column("email", db.String(120), nullable=False, unique=True)
    cpf = db.Column("cpf", db.String(12), nullable=False, unique=True)
    password_hash = db.Column("password_hash", db.Text, nullable=False)
    user_type = db.Column("user_type", db.String(100), nullable=False)
    phonenumber = db.Column("phonenumber", db.String(100))

    def __init__(self, name, email, cpf, password, default_role, phonenumber):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.set_password(password)
        self.user_type = default_role
        self.phonenumber = phonenumber

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)