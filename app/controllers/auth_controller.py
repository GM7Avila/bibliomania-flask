from flask import Blueprint, render_template, request
from flask_login import login_user

# Utils
from app.utils.validations import *
from app.utils.decorators import *

# Services
from app.services.user_service import user_service

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/")
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route("/sign-in", methods=["POST", "GET"])
@redirect_if_logged_in
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        found_user = user_service.findUserByEmail(email)

        if found_user and found_user.check_password(password):
            login_user(found_user)

            if found_user.isAdmin:
                return redirect(url_for("admin_book.acervo"))

            return redirect(url_for("book.acervo"))

        else:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for("auth.login"))

    return render_template("sign-in-template.html")

@auth_bp.route("/sign-up", methods=["POST", "GET"])
@redirect_if_logged_in
def signup():
    if request.method == "POST":
        name = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]

        if not all([name, cpf, email, password, phonenumber]):
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("auth.signup"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("auth.signup"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("auth.signup"))

        if user_service.findUserByEmail(email) or user_service.findUserByCPF(cpf):
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("auth.signup"))

        success = user_service.createUser(name, email, cpf, password, phonenumber)

        if success:
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Erro ao cadastrar o usuário.", "error")
            return redirect(url_for("auth.signup"))

    return render_template("sign-up-template.html")
