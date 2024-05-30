from app import db
from ..models.User import User

class UserController():
    def createUser(self, user):
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


    def readUser(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            return user
        except Exception as e:
            return None

    def updateUser(self, user_id, password=None, phone=None, name=None):
        try:
            user = db.session.query(User).get(user_id)
            if user:
                if password:
                    user.set_password(password)
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

    def deleteUser(self, user_id):
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