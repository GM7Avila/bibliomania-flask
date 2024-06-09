from flask import Blueprint, render_template
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

    for book in books:
        temp_books.append(bookMapper(book))

    return render_template("acervo-admin.html", books=temp_books, active_page='acervo')