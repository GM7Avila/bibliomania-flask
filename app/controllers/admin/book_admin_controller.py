from flask import Blueprint, render_template, request
from flask_login import login_required

# Utils
from app.utils.decorators import *
from app.utils.url_safer import *
from app.utils.mapper import bookMapper

# Services
from app.services.book_service import book_service
from app.services.reservation_service import reservation_service


admin_book_bp = Blueprint('admin_book', __name__, template_folder="../../templates/admin/book")

# Retorna todos os livros com o id hasheado
@admin_book_bp.route("/", methods=["POST", "GET"])
def acervo():
    books = book_service.getSortedBooksByAvailableStock()
    temp_books = []
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

    for book in books:
        temp_books.append(bookMapper(book))

    return render_template("acervo-admin.html", books=temp_books, active_page='acervo')