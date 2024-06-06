from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

# Services
from app.services.user_service import user_service

user_bp = Blueprint("user", __name__, template_folder="../templates/client/profile")
@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@user_bp.route('/')
@login_required
def profile():
    return render_template("pageuser.html", active_page='profile')

@user_bp.route("/alterar-senha", methods=["POST", "GET"])
@login_required
def change_password():
    if request.method == 'POST':
        action = request.form.get('action')

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash("Senha atual incorreta.", "error")
            return redirect(url_for("user.update_profile"))

        if new_password != confirm_password:
            flash("A nova senha e a confirmação da senha não coincidem.", "erro")
            return redirect(url_for("user.change_password"))

        success = user_service.changePassword(user_id=current_user.id, password=new_password)

        if success:
            flash("Senha alterada com sucesso!", "success")
        else:
            flash("Erro ao alterar a senha.", "error")

        return redirect(url_for("user.profile"))

    return render_template("change-password.html", active_page='profile')

@user_bp.route("/editar", methods=["POST", "GET"])
@login_required
def update_profile():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'Atualizar':
            name = request.form.get('input_nome')
            phonenumber = request.form.get('input_telefone')

            success = user_service.updateUser(
                user_id=current_user.id,
                name=name,
                phone=phonenumber
            )

            if success:
                flash("Usuário atualizado com sucesso!", "success")
                return redirect(url_for("user.profile"))
            else:
                flash("Erro ao atualizar o usuário.", "error")
                return redirect(url_for("user.update_profile"))

        elif action == 'Excluir Conta':
            success = user_service.deleteUser(user_id=current_user.id)

            if success:
                logout_user()
                flash("Conta apagada com sucesso.", "success")
                return redirect(url_for("user.login"))
            else:
                flash("Erro ao deletar o usuário.", "error")
                return redirect(url_for("user.profile"))

    return render_template("page-user-att.html", active_page='profile')
