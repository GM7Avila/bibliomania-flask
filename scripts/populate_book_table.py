from app import create_app, db
from app.models.book import Book
from app.models.genre import Genre
from app.models.genre_book import GenreBook
from sqlalchemy.exc import IntegrityError

app = create_app()

def populate_book_table():
    genres_data = [
        {"type": "Fantasia"},
        {"type": "Aventura"},
        {"type": "Romance"},
        {"type": "Ficção Científica"},
        {"type": "Mistério"},
        {"type": "Suspense"}
    ]

    for genre_data in genres_data:
        genre = Genre(**genre_data)
        db.session.add(genre)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # Reverte a transação para que possamos continuar

    books_data = [
        {"isbn": "1780439362139", "title": "Harry Potter and the Philosopher's Stone", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2001", "totalStock": 12, "availableStock": 12, "genre_type": "Fantasia"},
        {"isbn": "2780545582889", "title": "Harry Potter and the Chamber of Secrets", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2002", "totalStock": 10, "availableStock": 10, "genre_type": "Fantasia"},
        {"isbn": "3780439554930", "title": "Harry Potter and the Prisoner of Azkaban", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2003", "totalStock": 8, "availableStock": 8, "genre_type": "Fantasia"},
        {"isbn": "4780439136358", "title": "Harry Potter and the Goblet of Fire", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2005", "totalStock": 15, "availableStock": 15, "genre_type": "Fantasia"},
        {"isbn": "5780439785969", "title": "Harry Potter and the Order of the Phoenix", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2007", "totalStock": 20, "availableStock": 20, "genre_type": "Fantasia"},
        {"isbn": "6780545139700", "title": "Harry Potter and the Half-Blood Prince", "author": "J. K. Rowling",
         "publisher": "Scholastic", "year": "2009", "totalStock": 18, "availableStock": 18, "genre_type": "Fantasia"},
    ]

    for book_data in books_data:
        genre_type = book_data.pop("genre_type")
        genre = Genre.query.filter_by(type=genre_type).first()
        if genre:
            book = Book(**book_data)
            db.session.add(book)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_book_table()
