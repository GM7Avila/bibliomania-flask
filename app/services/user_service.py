from app import db
from app.models.user import User


class user_service():

    @staticmethod
    def createUser(name, email, cpf, password, phonenumber):
        try:

            # Só permite criação de clientes
            isAdmin = False

            user = User(name, email, cpf, password, isAdmin, phonenumber)
            db.session.add(user)
            db.session.commit()
            print(user)
            return True
        except Exception as e:
            db.session.rollback()
            print(user)
            print(e)
            return False

    @staticmethod
    def readUser(user_id):
        try:
            user = db.session.query(User).get(user_id)
            return user
        except Exception as e:
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
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
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
            return False

    @staticmethod
    def deleteUser(user_id):
        try:
            user = db.session.query(User).get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def findUserByEmail(email):
        try:
            user = db.session.query(User).filter_by(email=email).first()
            return user
        except Exception as e:
            print("Erro ao encontrar usuário pelo e-mail:", e)
            return None

    @staticmethod
    def findUserByCPF(cpf):
        try:
            user = db.session.query(User).filter_by(cpf=cpf).first()
            return user
        except Exception as e:
            return None

    @staticmethod
    def findUserByName(name):
        try:
            users = db.session.query(User).filter(User.name.like(f'%{name}%')).all()
            return users
        except Exception as e:
            return None

    @staticmethod
    def getAllUser():
        try:
            users = db.session.query(User).all()
            return users
        except Exception as e:
            return None