from app import db, login_manager
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
@login_manager.user_loader
def load_user(usuario_id):
    return User.query.get(int(usuario_id))

# @login_manager.request_loader
# def load_user_from_request(request):
#     auth_header = request.headers.get('Authorization')
#
#     if auth_header:
#         token = auth_header.replace('Bearer ', '')
#         user = User.query.filter_by(token=token).first()
#
#         if user:
#             return user
#
#     return None

class User(UserMixin, db.Model):

    __tablename__ = "user"

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(120), nullable=False)
    email = db.Column("email", db.String(120), nullable=False, unique=True)
    cpf = db.Column("cpf", db.String(12), nullable=False, unique=True)
    password_hash = db.Column("password_hash", db.Text, nullable=False)
    user_type = db.Column("user_type", db.String(100), nullable=False)
    phonenumber = db.Column("phonenumber", db.String(100))

    # reservation relation
    reservations = relationship("Reservation", back_populates="user")

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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return(self._id)