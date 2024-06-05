from flask import Blueprint, render_template, request, flash, url_for, redirect

# Services / Models
from app.services.book_service import book_service

book_bp = Blueprint('book', __name__, template_folder="templates")

@book_bp.route("/acervo", methods=["POST", "GET"])
def acervo():
    books = book_service.getSortedBooksByAvailableStock()
    return render_template("acervo.html", books=books, active_page='acervo')
