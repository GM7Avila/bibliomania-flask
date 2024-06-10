from flask import Blueprint, render_template, request
from flask_login import login_required

# Services
from app.services.book_service import book_service
from app.services.reservation_service import reservation_service
# Utils
from app.utils.decorators import *
from app.utils.mapper import bookMapper
from app.utils.url_safer import *

book_bp = Blueprint('book', __name__, template_folder="../../templates/client/book")


# Retorna todos os livros com o id hasheado
@book_bp.route("/", methods=["POST", "GET"])
@login_required
def acervo():
    if request.method == "POST":
        search = request.form.get("input-search")
        filtro_selecionado = request.form.get("filtro")

        if filtro_selecionado == "filtroTitulo":
            books = book_service.getBooksBySimilarTitle(search)
        elif filtro_selecionado == "filtroISBN":
            isbn = request.form.get("input-search")  # Obtendo o valor do ISBN do formulário
            book = book_service.getBookByISBN(isbn)  # Passando apenas o valor do ISBN
            books = [book] if book else []  # Se o livro for encontrado, coloque-o em uma lista; caso contrário, use uma lista vazia
        elif filtro_selecionado == "filtroTodos":
            books = book_service.getAllBooks()
        elif filtro_selecionado == "filtroAutor":
            books = book_service.getBooksByAuthor(author=search)
        else:
            # Se nenhum filtro válido for selecionado, renderize a página com uma lista vazia de livros
            books = []
            flash("Nenhum livro encontrado.", "danger")

    else:
        # Se não houver uma solicitação POST, isso significa que é uma solicitação GET.
        # Nesse caso, simplesmente obtenha todos os livros sem filtrar.
        books = book_service.getSortedBooksByAvailableStock()

    # Mapeie os livros para o formato desejado antes de passá-los para o template
    temp_books = [bookMapper(book) for book in books]

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
    can_reserve = not reservation_service.has_open_reservations(user_id)
    return render_template("reservation-confirm.html", book=book, can_reserve=can_reserve)


@book_bp.route("/reserve/<int:book_id>", methods=["POST"])
@login_required
def reservar(book_id):
    book = book_service.findBookById(book_id)

    if reservation_service.has_open_reservations(current_user.id):
        flash("Você já possui reservas abertas. Não é possível fazer uma nova reserva.", "danger")
    else:
        reservation = reservation_service.createReservation(current_user, book)
        if reservation:
            flash("Reserva realizada com sucesso!", "success")
        else:
            flash("Não foi possível realizar a reserva. Tente novamente.", "danger")
    return redirect(url_for("book.acervo"))
