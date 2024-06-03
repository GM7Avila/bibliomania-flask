from app import app
from flask import redirect, url_for, render_template, request, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from functools import wraps

# Utils & Scripts
from app.utils.validations import validate_email, validate_cpf
from scripts.populate_book_table import populate_book_table

# Controllers
from app.controllers.UserController import *
from app.controllers.ReservationController import *
from app.controllers.BookController import *

def redirect_if_logged_in(f):
    """
    Decorator function that redirects the user to the 'user' page if they are already logged in.

    Description:
        This decorator function checks if the current user is authenticated. If they are, it redirects them to the 'user' page.
        If they are not authenticated, it calls the decorated function and adds cache control headers to the response.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('acervo'))
        response = make_response(f(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return decorated_function

def redirect_if_no_stock(f):
    """
    Decorator function that redirects the user to the 'acervo' page if the book has no stock.

    Description:
        This decorator function checks if the book has available stock. If it doesn't, it redirects the user to the 'acervo' page.
        If it does, it calls the decorated function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        book_id = kwargs.get('book_id')
        book = BookController.getBookById(book_id)
        if book.availableStock == 0:
            flash("Este livro está indisponível para reserva.", "danger")
            return redirect(url_for('acervo'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return redirect(url_for("login"))


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
             SIGN IN AND SIGN UP ROUTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@app.route("/login", methods=["POST", "GET"])
@redirect_if_logged_in
def login():

    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        found_user = UserController.findUserByEmail(email)

        if found_user and found_user.check_password(password):
            login_user(found_user)
            return redirect(url_for("acervo"))
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

        if UserController.findUserByEmail(email) or UserController.findUserByCPF(cpf):
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        user = User(name, email, cpf, password, user_type, phonenumber)
        success = UserController.createUser(user)

        if success:
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
        else:
            flash("Erro ao cadastrar o usuário.", "error")
            return redirect(url_for("signup"))

    return render_template("sign-up-template.html")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                       USER ROUTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route("/acervo", methods=["POST", "GET"])
@login_required
def acervo():
    books = Book.query.all()  # Consulta todos os livros na tabela 'book'
    return render_template("acervo.html", books=books, active_page='acervo')

@app.route("/acervo/<int:book_id>", methods=["POST", "GET"])
@login_required
@redirect_if_no_stock
def reservation_confirm(book_id):
    book = BookController.getBookById(book_id)
    user_id = current_user.id
    can_reserve = not ReservationController.has_active_reservations(user_id)
    return render_template("reservation_confirm.html", book=book,can_reserve=can_reserve)

@app.route("/reservar/<int:book_id>", methods=["POST"])
@login_required
@redirect_if_no_stock
def reservar(book_id):
    book = BookController.getBookById(book_id)
    if book and book.availableStock > 0:
        user_id = current_user.id
        can_reserve = ReservationController.has_active_reservations(user_id)

        if can_reserve:
            flash("Você já possui reservas ativas. Não é possível fazer uma nova reserva.", "danger")
        else:
            reservation = ReservationController.createReservation(user_id, book_id)
            if reservation:
                flash("Reserva realizada com sucesso!", "success")
            else:
                flash("Não foi possível realizar a reserva. Tente novamente.", "danger")
    else:
        flash("Livro não encontrado.", "danger")
    return redirect(url_for("acervo"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/profile')
@login_required
def profile():
    return render_template("pageuser.html", active_page='profile')

@app.route("/profile/att/change-password", methods=["POST", "GET"])
@login_required
def change_password():
    if request.method == 'POST':
        action = request.form.get('action')

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash("Senha atual incorreta.", "error")
            return redirect(url_for("update_profile"))

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


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    RESERVATION ROUTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
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
    return render_template("reservation-details.html", reservation=reservation, can_renew=can_renew)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                       BOOK ROUTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                       APP CONFIG
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
with app.app_context():
    db.create_all()
    populate_book_table()

if __name__ == "__main__":
    app.run(debug=True)

