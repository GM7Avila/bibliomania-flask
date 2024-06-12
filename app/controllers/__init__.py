def register_blueprints(app):
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user.book_controller import book_bp
    from app.controllers.user.user_controller import user_bp
    from app.controllers.user.reservation_controller import reservation_bp

    from app.controllers.admin.book_admin_controller import admin_book_bp
    from app.controllers.admin.user_admin_controller import admin_user_bp
    from app.controllers.admin.reservation_admin_controller import admin_reservation_bp

    # auth
    app.register_blueprint(auth_bp, url_prefix='/')

    # user
    app.register_blueprint(book_bp, url_prefix='/acervo')
    app.register_blueprint(user_bp, url_prefix='/perfil')
    app.register_blueprint(reservation_bp, url_prefix='/reservas')

    # admin
    app.register_blueprint(admin_book_bp, url_prefix='/admin/acervo')
    app.register_blueprint(admin_user_bp, url_prefix='/admin/perfil')
    app.register_blueprint(admin_reservation_bp, url_prefix='/admin/reservas')