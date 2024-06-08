import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root@localhost/bibliomania')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_ROUTES = ['/admin/acervo/', '/admin/perfil/', '/admin/reservas/']

    USER_ROUTES = ['/acervo/', '/perfil/', '/reservas/']

    PUBLIC_ROUTES = ['/sign-in', '/sign-up', '/']
