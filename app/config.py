import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root@localhost/bibliomania')
    SQLALCHEMY_TRACK_MODIFICATIONS = False