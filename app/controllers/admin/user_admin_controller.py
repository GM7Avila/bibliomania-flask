from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, logout_user

from app.utils.decorators import *
from app.utils.mapper import userMapper
from app.utils.url_safer import *

# Services
from app.services.user_service import user_service

admin_user_bp = Blueprint("admin_user", __name__, template_folder="../../templates/admin/profile")

@admin_user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@admin_user_bp.route('/', methods=["POST", "GET"])
def profile_adm():
    users = user_service.getAllUser()
    temp_users = [userMapper(user) for user in users] if users else []
    return render_template("pageuser-admin.html", users=temp_users, active_page='profile')

@admin_user_bp.route("/u=<token>", methods=["GET", "POST"])
@login_required
def user_edit(token):
    user_id = decode_id(token)
    user = user_service.getUserById(user_id)
    if user is None:
        return redirect(url_for("admin_user.profile_adm"))
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Atualizar':
            name = request.form.get('name')
            phonenumber = request.form.get('phonenumber')

            success = user_service.updateUser(
                user_id=user.id,
                name=name,
                phone=phonenumber
            )

            if success:
                flash("Usuário atualizado com sucesso!", "success")
                return redirect(url_for("admin_user.profile_adm"))
            else:
                flash("Erro ao atualizar o usuário.", "error")
                return redirect(url_for("admin_user.user_edit", token=token))

        elif action == 'Excluir Conta':
            success = user_service.deleteUser(user_id)
            if success:
                flash("Usuário apagado com sucesso!", "success")
                return redirect(url_for("admin_user.profile_adm"))
            else:
                flash("Erro ao apagar o usuário.", "error")
                return redirect(url_for("admin_user.user_edit", token=token))

    return render_template("edit-user.html", user=user, token=token)
