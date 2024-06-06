from flask import redirect, url_for, flash, make_response
from flask_login import current_user
from functools import wraps
from ..services.book_service import book_service

# Authentication
def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('book.acervo'))
        response = make_response(f(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return decorated_function


# Books
def redirect_if_no_stock(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        book_id = kwargs.get('book_id')
        book = book_service.findBookById(book_id)
        if book.availableStock == 0:
            flash("Este livro está indisponível para reserva.", "danger")
            return redirect(url_for('book.list_books'))
        return f(*args, **kwargs)
    return decorated_function
