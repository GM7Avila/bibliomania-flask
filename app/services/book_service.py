from app import db
from app.models.book import Book
from app.models.genre_book import GenreBook
from app.models.genre import Genre

class book_service:

    # =================== CREATE UPDATE AND DELETE ===================
    # CREATE
    @staticmethod
    def createBook(isbn, title, author, publisher, year, totalStock, availableStock):
        try:
            book = Book(isbn, title, author, publisher, year, totalStock, availableStock)
            db.session.add(book)
            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            return None

    # UPDATE
    @staticmethod
    def updateBook(book_id, isbn=None, title=None, author=None, publisher=None, year=None, totalStock=None,
                   availableStock=None):
        try:
            book = Book.query.get(book_id)
            if not book:
                return None

            if isbn is not None:
                book.isbn = isbn
            if title is not None:
                book.title = title
            if author is not None:
                book.author = author
            if publisher is not None:
                book.publisher = publisher
            if year is not None:
                book.year = year
            if totalStock is not None:
                book.totalStock = totalStock
            if availableStock is not None:
                book.availableStock = availableStock

            db.session.commit()
            return book
        except Exception as e:
            db.session.rollback()
            return None

    # DELETE
    @staticmethod
    def deleteBook(book_id):
        try:
            book = Book.query.get(book_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False


    # ==================================== READ ====================================
    """
    Get Books: Retorna uma lista de Livros
    """

    # 1. Retorna todos os livros
    @staticmethod
    def getAllBooks():
        try:
            books = Book.query.all()
            return books
        except Exception as e:
            return None

    # 2. Recebe um Titulo e retorna uma lista de livros com nomes similares
    @staticmethod
    def getBooksBySimilarTitle(title):
        try:
            books = Book.query.filter(Book.title.ilike(f'%{title}%')).all()
            return books
        except Exception as e:
            print(f"Erro ao buscar livros por título: {e}")
            return None

    # 3. Recebe um autor e retorna uma lista de livros
    @staticmethod
    def getBooksByAuthor(author):
        try:
            books = Book.query.filter_by(author=author).all()
            return books
        except Exception as e:
            return None

    @staticmethod
    def getBooksByGenreId(genre_id):
        try:
            genre_books = GenreBook.query.filter_by(genre_id=genre_id).all()
            books = [genre_book.book for genre_book in genre_books]
            return books
        except Exception as e:
            return None

    @staticmethod
    def getAllGenres():
        try:
            genres = Genre.query.all()
            return genres
        except Exception as e:
            return None

    @staticmethod
    def getAllGenreBooks():
        try:
            genre_books = GenreBook.query.all()
            return genre_books
        except Exception as e:
            return None

    # 4. Recebe um ISBN e retorna um livro
    @staticmethod
    def getBookByISBN(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first()
            return book
        except Exception as e:
            return None

    # 5. Retorna livros ordenados pela disponibildiade no estoque
    @staticmethod
    def getSortedBooksByAvailableStock():
        try:
            books = db.session.query(Book).order_by(
                Book.isAvailable.desc(),
                Book.availableStock.desc(),
                Book.title
            ).all()

            return books
        except Exception as e:
            return None

    """
    Get Books: Retorna uma lista de Livros
    """

    # 1. Recebe um ISBN e retorna um livro
    @staticmethod
    def findBookByISBN(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first()
            return book
        except Exception as e:
            return None

    # 2. Recebe um Titulo e retorna um livro
    @staticmethod
    def findBookByTitle(title):
        try:
            book = Book.query.filter_by(title=title).all()
            return book
        except Exception as e:
            return None

    # 3. Recebe um ID e retorna um Livro
    @staticmethod
    def findBookById(book_id):
        try:
            book = Book.query.get(book_id)
            return book
        except Exception as e:
            return None
