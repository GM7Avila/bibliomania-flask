from flask import redirect, url_for, render_template, request, flash, make_response
from functools import wraps
from app.utils.validations import validate_email, validate_cpf
from app import app, db
from scripts.populate_book_table import populate_book_table
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

# Modelos
from app.models.User import User
from app.models.Reservation import Reservation

# Controllers
from app.controllers.UserController import *
from app.controllers.ReservationController import *

user_controller = UserController()

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

        found_user = db.session.query(User).filter_by(email=email).first()
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

        if db.session.query(User).filter_by(email=email).first() or db.session.query(User).filter_by(cpf=cpf).first():
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        user = User(name, email, cpf, password, user_type, phonenumber)
        success = user_controller.createUser(user)

        if success:
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
        else:
            flash("Erro ao cadastrar o usuário.", "error")
            return redirect(url_for("signup"))

    return render_template("sign-up-template.html")

@app.route('/profile')
@login_required
def profile():
    return render_template("pageuser.html", active_page='profile')

@app.route("/profile/att/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    if request.method == 'POST':
        action = request.form.get('action')

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash("Senha atual incorreta.", "error")
            return redirect(url_for("change_password"))

        if new_password != confirm_password:
            flash("A nova senha e a confirmação da senha não coincidem.", "erro")
            return redirect(url_for("change_password"))

        success = UserController.changePassword(user_id=current_user.id, password=new_password)

        if success:
            flash("Senha alterada com sucesso!", "success")
        else:
            flash("Erro ao alterar a senha.", "error")

        return redirect(url_for("profile"))

    return render_template("change-password.html", active_page='profile')
@app.route("/profile/att", methods=["POST", "GET"])
@login_required
def update_profile():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'Atualizar':
            name = request.form.get('input_nome')
            phonenumber = request.form.get('input_telefone')

            success = UserController.updateUser(
                user_id=current_user.id,
                name=name,
                phone=phonenumber
            )

            if success:
                flash("Usuário atualizado com sucesso!", "success")
                return redirect(url_for("profile"))
            else:
                flash("Erro ao atualizar o usuário.", "error")
                return redirect(url_for("update_profile"))

        elif action == 'Excluir Conta':
            success = UserController.deleteUser(user_id=current_user.id)

            if success:
                logout_user()
                flash("Conta apagada com sucesso.", "success")
                return redirect(url_for("login"))
            else:
                flash("Erro ao deletar o usuário.", "error")
                return redirect(url_for("profile"))

    return render_template("page-user-att.html", active_page='profile')


@app.route("/reservation", methods=["POST", "GET"])
@login_required
def reservation():

    if request.method == "POST":
        search = request.form.get("input-search")
        reservations = []

        filtro_selecionado = request.form.get("filtro")

        if filtro_selecionado == "filtroStatus":
            reservations = ReservationController.getUserReservationsByStatus(user_id=current_user.id, status=search)

        elif filtro_selecionado == "filtroISBN":
            reservations = ReservationController.getUserReservationsByBookISBN(user_id=current_user.id, isbn=search)

        elif filtro_selecionado == "filtroTitulo":
            reservations = ReservationController.getUserReservationsByBookTitle(user_id=current_user.id, title=search)

        elif filtro_selecionado == "filtroTodos":
            reservations = ReservationController.getReservationsByUser(user_id=current_user.id)

        return render_template("reservation-list.html", active_page='reservation', reservations=reservations)

    if request.method == "GET":
        reservations = ReservationController.getReservationsByUser(user_id=current_user.id)
        return render_template("reservation-list.html", active_page='reservation', reservations=reservations)

# TODO: funcionalidades do banco no controller

@app.route("/reservation/<int:reservation_id>", methods=["GET", "POST"])
@login_required
def reservation_detail(reservation_id):

    reservation = Reservation.query.get(reservation_id)

    if reservation is None:
        return render_template(url_for("reservation"))

    ReservationController.updateStatus(reservation_id)

    if request.method == "POST":
        if request.form.get("action") == "renew":
            if reservation.status == "Ativa" and reservation.expirationDate >= date.today() and reservation.renewCount < 3:
                success = ReservationController.renewReservation(reservation)
                if success:
                    flash("Reserva renovada com sucesso!", "success")
                else:
                    flash("Erro ao renovar a reserva.", "error")
            else:
                flash("Não é possível renovar a reserva. A reserva está atrasada ou finalizada.", "error")
        return render_template("reservation-details.html", reservation=reservation)

    can_renew = reservation.status == "Ativa" and reservation.expirationDate >= date.today() and reservation.renewCount < 3
    return render_template("reservation-details.html", reservation=reservation, can_renew=can_renew, active_page='reservation')

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