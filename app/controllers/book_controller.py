from flask import Blueprint, render_template
from flask_login import login_required

# Utils
from app.utils.decorators import *
from app.utils.url_safer import *
from app.utils.mapper import bookMapper

# Services
from app.services.book_service import book_service
from app.services.reservation_service import reservation_service

book_bp = Blueprint('book', __name__, template_folder="../templates/client/book")

# Retorna todos os livros com o id hasheado
@book_bp.route("/", methods=["POST", "GET"])
@login_required
def acervo():
    books = book_service.getSortedBooksByAvailableStock()
    temp_books = []

    # for book in books:
    #     book.id = encode_id(book.id)

    for book in books:
        temp_books.append(bookMapper(book))

    return render_template("acervo.html", books=temp_books, active_page='acervo')


@book_bp.route("/livro-<token>", methods=["POST", "GET"])
@login_required
def reservation_confirm(token):
    book_id = decode_id(token)
    if book_id is None:
        # Lógica para lidar com token inválido
        flash("Token inválido.", "danger")
        return redirect(url_for("book.acervo"))

    book = book_service.findBookById(book_id)
    if book is None:
        # Lógica para lidar com livro não encontrado
        flash("Livro não encontrado.", "danger")
        return redirect(url_for("book.acervo"))

    user_id = current_user.id
    can_reserve = not reservation_service.has_active_reservations(user_id)
    return render_template("reservation-confirm.html", book=book, can_reserve=can_reserve)


@book_bp.route("/reserve/<int:book_id>", methods=["POST"])
@login_required
def reservar(book_id):
    book = book_service.findBookById(book_id)

    if reservation_service.has_active_reservations(current_user.id):
        flash("Você já possui reservas ativas. Não é possível fazer uma nova reserva.", "danger")
    else:
        reservation = reservation_service.createReservation(current_user, book)
        if reservation:
            flash("Reserva realizada com sucesso!", "success")
        else:
            flash("Não foi possível realizar a reserva. Tente novamente.", "danger")
    return redirect(url_for("book.acervo"))
