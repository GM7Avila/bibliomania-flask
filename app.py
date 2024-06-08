from flask import request
from app import create_app
from app import login_manager
from flask_login import current_user

app = create_app()

# Middleware para verificar as permissões de acesso aos controllers: acontece antes de todas as requisições
@app.before_request
def check_controller_permissions():

    require_admin = False
    require_user = False

    for route in app.config['ADMIN_ROUTES']:
        if request.path == route:
           require_admin = True

    for route in app.config['USER_ROUTES']:
        if request.path == route:
           require_user = True

    print(request.path)
    print(request.endpoint)
    print(request.full_path)
    print(request.host_url)
    print(request.url)
    print(request.base_url)
    print(request.root_url)
    print(request.root_path)
    print(require_admin)
    print(require_user)

    # if require_admin and not current_user.is_authenticated:
    #     return login_manager.unauthorized()
    # if require_admin and not current_user.isAdmin:
    #     return "Acesso negado para este controller."
    #
    # require_client = app.config['CONTROLLER_USER_PERMISSIONS'].get(request.path)
    #
    # if require_client and not current_user.is_authenticated:
    #     return login_manager.unauthorized()
    # if require_client and current_user.isAdmin:
    #     return "Acesso negado para este controller."

    return None

if __name__ == "__main__":
    app.run(debug=True)