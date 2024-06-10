from flask import Blueprint, render_template, request
from flask_login import login_required, logout_user
from app.utils.decorators import *
from app.utils.mapper import userMapper

# Services
from app.services.user_service import user_service


admin_user_bp = Blueprint("admin_user", __name__, template_folder="../../templates/admin/profile")

@admin_user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@login_required
@admin_user_bp.route('/', methods=["POST", "GET"])
def profile_adm():

    users = user_service.getAllUser()
    temp_users = []

    if request.method == "POST":
        search = request.form.get("input-search")
        filtro_selecionado = request.form.get("filtro")

        if filtro_selecionado == "filtroNome":
           users = user_service.findUserByName(search)
        elif filtro_selecionado == "filtroCPF":
            users = user_service.findUserByCPF(search)
        elif filtro_selecionado == "filtroEmail":
            users = user_service.findUserByEmail(search)

    for user in users:
        temp_users.append(userMapper(user))
    return render_template("pageuser-admin.html", users=temp_users, active_page='profile')