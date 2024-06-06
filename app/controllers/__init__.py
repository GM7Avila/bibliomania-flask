def register_blueprints(app):

    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.reservation_controller import reservation_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(book_bp, url_prefix='/acervo')
    app.register_blueprint(user_bp, url_prefix='/perfil')
    app.register_blueprint(reservation_bp, url_prefix='/reservas')
