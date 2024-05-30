from flask import redirect, url_for, render_template, request, flash, make_response
from functools import wraps
from app.utils.validations import validate_email, validate_cpf
from app.models.User import User
from app import app, db
from scripts.populate_book_table import populate_book_table
from app.models.Reservation import Reservation
from datetime import datetime
from app.models.Book import Book
from flask_login import login_user, logout_user, login_required, current_user

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('user'))
        response = make_response(f(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
@redirect_if_logged_in
def login():
    flash("")

    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        found_user = User.query.filter_by(email=email).first()
        if found_user and found_user.check_password(password):
            login_user(found_user)
            return redirect(url_for("user"))
        else:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for("login"))

    return render_template("sign-in-template.html")


@app.route("/signup", methods=["POST", "GET"])
@redirect_if_logged_in
def signup():

    if request.method == "POST":
        nome = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]

        if not all([nome, cpf, email, password, phonenumber]):
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("signup"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("signup"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first() or User.query.filter_by(cpf=cpf).first():
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        try:
            new_user = User(nome, email, cpf, password, "user", phonenumber)
            db.session.add(new_user)
            db.session.commit()
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Erro ao cadastrar o usuário.", "error")
            app.logger.error(f"Erro ao cadastrar usuário: {e}")
            return redirect(url_for("signup"))

    return render_template("sign-up-template.html")


@app.route("/profile/att", methods=["POST", "GET"])
@login_required
def update_profile():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'Atualizar':
            # Executando comando de atualização de dados
            name = request.form.get('input_nome')
            cpf = request.form.get('input_cpf')
            email = request.form.get('input_email')
            phonenumber = request.form.get('input_telefone')

            # Validação dos dados
            if not all([name, cpf, email, phonenumber]):
                flash("Por favor, preencha todos os campos.", "error")
                return redirect(url_for("update_profile"))

            if not validate_email(email):
                flash("E-mail inválido.", "error")
                return redirect(url_for("update_profile"))

            if not validate_cpf(cpf):
                flash("CPF inválido.", "error")
                return redirect(url_for("update_profile"))

            existing_email = User.query.filter_by(email=email).first()
            existing_cpf = User.query.filter_by(cpf=cpf).first()

            try:
                current_user.name = name
                current_user.cpf = cpf
                current_user.email = email
                current_user.phonenumber = phonenumber

                db.session.commit()
                flash("Usuário atualizado com sucesso!", "success")
                return redirect(url_for("profile"))
            except Exception as e:
                flash("Erro ao atualizar o usuário.", "error")
                app.logger.error(f"Erro ao atualizar usuário: {e}")
                return redirect(url_for("update_profile"))

        elif action == 'Excluir Conta':
            # Executando comando de deletar
            try:
                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                flash("Usuário deletado com sucesso.", "success")
                return redirect(url_for("login"))
            except Exception as e:
                flash("Erro ao deletar o usuário.", "error")
                app.logger.error(f"Erro ao deletar usuário: {e}")
                return redirect(url_for("profile"))

    return render_template("page-user-att.html", active_page='profile')


@app.route('/profile')
@login_required
def profile():
    return render_template("pageuser.html", active_page='profile')


@app.route("/reservation")
@login_required
def reservation():
    return render_template("reservation.html",active_page='reservation')


@app.route("/user")
@login_required
def user():
    return render_template("base.html",active_page='user')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/create-reservation")
@login_required
def create_reservation():
    # Data atual
    current_date = datetime.now().date()

    # Criando uma reserva com valores fictícios
    reservation = Reservation(
        reservationDate=current_date,
        expirationDate=current_date,
        status="Ativa",
        user_id=1,  # Substitua pelo ID do usuário correto
        book_id=1   # Substitua pelo ID do livro correto
    )

    # Adicione a reserva ao banco de dados
    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for("login"))

"""
ROTAS BOOK
"""

"""
CONFIG
"""
with app.app_context():
    db.create_all()
    populate_book_table()

if __name__ == "__main__":
    app.run(debug=True)