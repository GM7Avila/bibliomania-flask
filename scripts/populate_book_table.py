from app import app, db
from app.models.Book import Book
from sqlalchemy.exc import IntegrityError


def populate_book_table():
    books_data = [
        {"isbn": "1780439362139", "title": "Harry Potter and the Philosopher's Stone", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2001", "totalStock": 12, "availableStock": 12},
        {"isbn": "2780545582889", "title": "Harry Potter and the Chamber of Secrets", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2002", "totalStock": 10, "availableStock": 10},
        {"isbn": "3780439554930", "title": "Harry Potter and the Prisoner of Azkaban", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2003", "totalStock": 8, "availableStock": 8},
        {"isbn": "4780439136358", "title": "Harry Potter and the Goblet of Fire", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2005", "totalStock": 15, "availableStock": 15},
        {"isbn": "5780439785969", "title": "Harry Potter and the Order of the Phoenix", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2007", "totalStock": 20, "availableStock": 20},
        {"isbn": "6780545139700", "title": "Harry Potter and the Half-Blood Prince", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2009", "totalStock": 18, "availableStock": 18}
    ]

    for book_data in books_data:
        book = Book(**book_data)
        db.session.add(book)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # Reverte a transação para que possamos continuar

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        populate_book_table()
