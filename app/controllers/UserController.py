from app import db
from ..models.User import User

class UserController():

    @staticmethod
    def createUser(user):
        try:
            db.session.add(user)
            db.session.commit()
            print(user)
            print("crie")
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