from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.validations import validate_email, validate_cpf

# Services / Models
from app.models.user import User
from app.services.user_service import user_service

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        found_user = user_service.findUserByEmail(email)

        if found_user and found_user.check_password(password):
            login_user(found_user)
            return redirect(url_for("acervo"))
        else:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for("login"))

    return render_template("sign-in-template.html")

@auth_bp.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        name = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]
        user_type = "client"

        if not all([name, cpf, email, password, phonenumber]):
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("signup"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("signup"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("signup"))

        if user_service.findUserByEmail(email) or user_service.findUserByCPF(cpf):
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        user = User(name, email, cpf, password, user_type, phonenumber)
        success = user_service.createUser(user)

        if success:
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
        else:
            flash("Erro ao cadastrar o usuário.", "error")
            return redirect(url_for("signup"))

    return render_template("sign-up-template.html")
