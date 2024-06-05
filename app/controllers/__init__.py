from app.controllers.book_controller import book_bp
from app.controllers.user_controller import user_bp
from app.controllers.reservation_controller import reservation_bp
from app.controllers.auth_controller import auth_bp

def register_blueprints(app):
    app.register_blueprint(book_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(auth_bp)
