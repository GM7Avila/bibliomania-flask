from flask import Blueprint, render_template, request

# Modelo + Service
from app.models.book import Book
from app.services.book_service import *

# Blueprint
book_blueprint = Blueprint("book", __name__, template_folder="templates")

# Endpoints

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                       BOOK ROUTES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
@book_blueprint.route("/acervo", methods=["POST", "GET"])
def acervo():

    books = BookController.getSortedBooksByAvailableStock()
    return render_template("acervo.html", books=books, active_page='acervo')

@book_blueprint("/acervo/<int:book_id>", methods=["POST", "GET"])
def reservation_confirm(book_id):
    book = BookController.findBookById(book_id)
    user_id = current_user.id
    can_reserve = not ReservationController.has_active_reservations(user_id)
    return render_template("reservation-confirm.html", book=book,can_reserve=can_reserve)

@book_blueprint("/reservar/<int:book_id>", methods=["POST"])
def reservar(book_id):
    book = BookController.findBookById(book_id)
    user_id = current_user.id

    if ReservationController.has_active_reservations(user_id):
        flash("Você já possui reservas ativas. Não é possível fazer uma nova reserva.", "danger")
    else:
        reservation = ReservationController.createReservation(current_user, book)
        if reservation:
            flash("Reserva realizada com sucesso!", "success")
        else:
            flash("Não foi possível realizar a reserva. Tente novamente.", "danger")
    return redirect(url_for("acervo"))