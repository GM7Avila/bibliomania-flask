from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, logout_user
from app.utils.validations import validate_email, validate_cpf

from app.utils.decorators import *
from app.utils.format_mask import *
from app.utils.mapper import userMapper
from app.utils.url_safer import *

# Services
from app.services import user_service, reservation_service

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
            users = [user for user in users if user.name == search]
        elif filtro_selecionado == "filtroCPF":
            users = [user for user in users if user.cpf == search or format_cpf(user.cpf) == search]
        elif filtro_selecionado == "filtroEmail":
            users = [user for user in users if user.email == search]

    for user in users:
        user_data = userMapper(user)
        user_data['inadimplente'] = reservation_service.has_open_reservations(user.id)
        temp_users.append(user_data)

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
        print(f"Received action: {action}")
        if action == 'Atualizar':
            name = request.form.get('name')
            phonenumber = request.form.get('phonenumber')
            email = request.form.get('email')

            success = user_service.updateUserAdm(
                user_id=user.id,
                name=name,
                phone=phonenumber,
                email=email
            )

            if success:
                flash("Usuário atualizado com sucesso!", "success")
                return redirect(url_for("admin_user.profile_adm"))
            else:
                flash("Erro ao atualizar o usuário.", "error")
                return redirect(url_for("admin_user.user_edit", token=token))

        elif action == 'Excluir Conta':
            print(f"Attempting to delete user with ID: {user_id}")
            success = user_service.deleteUser(user_id)
            if success:
                flash("Usuário apagado com sucesso!", "success")
                return redirect(url_for("admin_user.profile_adm"))
            else:
                flash("Erro ao apagar o usuário. O usuário tem reservas não finalizadas.", "error")
                return redirect(url_for("admin_user.user_edit", token=token))

    return render_template("edit-user.html", user=user, token=token)

@admin_user_bp.route("/registro", methods=["POST", "GET"])
@login_required
def register():
    if request.method == "POST":
        name = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]

        if not all([name, cpf, email, password, phonenumber]):
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("admin_user.register"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("admin_user.register"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("admin_user.register"))

        if user_service.findUserByEmail(email) or user_service.findUserByCPF(cpf):
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("admin_user.register"))

        success = user_service.createUser(name, email, cpf, password, phonenumber)

        if success:
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("admin_user.profile_adm"))
        else:
            flash("Erro ao cadastrar o usuário.", "error")
            return redirect(url_for("admin_user.register"))

    return render_template("register.html")



