from flask import request, redirect, url_for
from app import create_app
from flask_login import current_user

app = create_app()

# Middleware para verificar as permissões de acesso aos controllers: acontece antes de todas as requisições
@app.before_request
def check_controller_permissions():
    public_routes = app.config['PUBLIC_ROUTES'] + app.config['PUBLIC_AUTH_ROUTES']
    if any(request.path.startswith(route) for route in public_routes):
        return None

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if request.path in app.config['ADMIN_ROUTES']:
        if not current_user.isAdmin:
            return "Access Denied", 403

    elif request.path in app.config['USER_ROUTES']:
        if current_user.isAdmin:
            return "Access Denied: Fora do escopo de admin", 403

    return None

if __name__ == "__main__":
    app.run(debug=True)
