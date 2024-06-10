from app import db
from app.models.user import User

class user_service:

    @staticmethod
    def createUser(name, email, cpf, password, phonenumber):
        try:
            isAdmin = False
            user = User(name=name, email=email, cpf=cpf, password=password, isAdmin=isAdmin, phonenumber=phonenumber)
            db.session.add(user)
            db.session.commit()
            print(f"User created: {user}")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return False

    @staticmethod
    def readUser(user_id):
        try:
            user = db.session.query(User).get(user_id)
            return user
        except Exception as e:
            print(f"Error reading user {user_id}: {e}")
            return None

    @staticmethod
    def updateUser(user_id, phone=None, name=None):
        try:
            user = User.query.get(user_id)
            if user:
                if phone:
                    user.phonenumber = phone
                if name:
                    user.name = name
                db.session.commit()
                print(f"User updated: {user}")
                return True
            else:
                print(f"User {user_id} not found for update.")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user {user_id}: {e}")
            return False

    @staticmethod
    def changePassword(user_id, password):
        try:
            user = User.query.get(user_id)
            if user:
                if password:
                    user.set_password(password)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error changing password for user {user_id}: {e}")
            return False

    @staticmethod
    def deleteUser(user_id):
        try:
            user = db.session.query(User).get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                print(f"User deleted: {user}")
                return True
            else:
                print(f"User {user_id} not found for deletion.")
                return False
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user {user_id}: {e}")
            return False

    @staticmethod
    def findUserByEmail(email):
        try:
            user = db.session.query(User).filter_by(email=email).first()
            return user
        except Exception as e:
            print(f"Error finding user by email {email}: {e}")
            return None

    @staticmethod
    def findUserByCPF(cpf):
        try:
            user = db.session.query(User).filter_by(cpf=cpf).first()
            return user
        except Exception as e:
            print(f"Error finding user by CPF {cpf}: {e}")
            return None

    @staticmethod
    def findUserByName(name):
        try:
            user = db.session.query(User).filter(User.name.like(f'%{name}%')).first()
            return user
        except Exception as e:
            print(f"Error finding user by name {name}: {e}")
            return None

    @staticmethod
    def getAllUser():
        try:
            users = db.session.query(User).all()
            return users
        except Exception as e:
            print(f"Error getting all users: {e}")
            return None

    @staticmethod
    def getUserById(user_id):
        try:
            user = User.query.get(user_id)
            return user
        except Exception as e:
            print(f"Error getting user by ID {user_id}: {e}")
            return None
