from app import db
from ..models.Book import Book
from sqlalchemy import case

class BookController:

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

    @staticmethod
    def getBookById(book_id):
        try:
            book = Book.query.get(book_id)
            return book
        except Exception as e:
            return None

    @staticmethod
    def getAllBooks():
        try:
            books = Book.query.all()
            return books
        except Exception as e:
            return None

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

    @staticmethod
    def findBookByISBN(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first()
            return book
        except Exception as e:
            return None

    @staticmethod
    def findBooksByAuthor(author):
        try:
            books = Book.query.filter_by(author=author).all()
            return books
        except Exception as e:
            return None

    @staticmethod
    def findBooksByTitle(title):
        try:
            books = Book.query.filter_by(title=title).all()
            return books
        except Exception as e:
            return None
