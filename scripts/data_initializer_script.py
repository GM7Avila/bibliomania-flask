import sys
import os

# Adiciona o path do projeto para o sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.book import Book
from app.models.genre import Genre
from app.models.genre_book import GenreBook
from app.models.user import User
from sqlalchemy.exc import IntegrityError

app = create_app()

def initializer_book_context():

    admin = User(
        name="Admin",
        email="admin@bibliomania",
        cpf=11111111111,
        password="admin",
        isAdmin = True,
        phonenumber = "11111111111"
    )

    db.session.add(admin)
    db.session.commit()

    genres_data = [
        {"genre_type": "Fantasia"},
        {"genre_type": "Aventura"},
        {"genre_type": "Romance"},
        {"genre_type": "Ficção Científica"},
        {"genre_type": "Mistério"},
        {"genre_type": "Suspense"}
    ]

    for genre_data in genres_data:
        genre = Genre(**genre_data)
        db.session.add(genre)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()  # Reverte a transação para que possamos continuar

    books_data = [
        {
            "isbn": "1780439362139",
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2001",
            "totalStock": 12,
            "availableStock": 12,
            "genre_type": "Fantasia",
            "description": "Discover the magical world of Hogwarts alongside Harry Potter, an orphaned boy who learns he is a wizard. In his first adventure, Harry faces mysterious challenges, makes unforgettable friends, and uncovers secrets that will change his life forever. Join him as he unravels the mystery of the Philosopher's Stone and finds his place in the magical world."
        },
        {
            "isbn": "2780545582889",
            "title": "Harry Potter and the Chamber of Secrets",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2002",
            "totalStock": 10,
            "availableStock": 10,
            "genre_type": "Fantasia",
            "description": "Return to Hogwarts with Harry Potter in his second year, where new dangers lurk in the school's corridors. Strange messages appear on the walls and students are being petrified. Harry and his friends, Hermione and Ron, must solve the mystery of the Chamber of Secrets to save the school and their fellow students from a terrible fate."
        },
        {
            "isbn": "3780439554930",
            "title": "Harry Potter and the Prisoner of Azkaban",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2003",
            "totalStock": 8,
            "availableStock": 8,
            "genre_type": "Fantasia",
            "description": "In Harry Potter's third year at Hogwarts, a new threat emerges in the form of Sirius Black, a fugitive believed to be after Harry. With new spells, magical creatures, and surprising revelations about his past, Harry faces closer dangers than ever before while uncovering truths about his family."
        },
        {
            "isbn": "4780439136358",
            "title": "Harry Potter and the Goblet of Fire",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2005",
            "totalStock": 15,
            "availableStock": 15,
            "genre_type": "Fantasia",
            "description": "In his fourth adventure, Harry Potter is unexpectedly selected to compete in the Triwizard Tournament, a deadly competition among wizarding schools. With frightening challenges and hidden enemies, Harry must prove his bravery and skill. The Goblet of Fire not only tests his abilities but also prepares him for the growing darkness threatening the wizarding world."
        },
        {
            "isbn": "5780439785969",
            "title": "Harry Potter and the Order of the Phoenix",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2007",
            "totalStock": 20,
            "availableStock": 20,
            "genre_type": "Fantasia",
            "description": "As Voldemort's return becomes undeniable, Harry Potter finds himself isolated and discredited by the Ministry of Magic. Alongside his friends, he forms Dumbledore's Army to teach defense against the dark arts. With the Order of the Phoenix working in the shadows, Harry faces painful losses and grows as a leader in his fight against the forces of evil."
        },
        {
            "isbn": "6780545139700",
            "title": "Harry Potter and the Half-Blood Prince",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2009",
            "totalStock": 18,
            "availableStock": 18,
            "genre_type": "Fantasia",
            "description": "As Voldemort tightens his grip on both the wizarding and Muggle worlds, Harry and Dumbledore work to uncover the dark secrets of the Dark Lord's past. In his sixth year at Hogwarts, Harry discovers a mysterious book belonging to the Half-Blood Prince, leading to more questions and discoveries about his ultimate enemy."
        }
    ]

    for book_data in books_data:
        genre_type = book_data.pop("genre_type")
        genre = Genre.query.filter_by(genre_type=genre_type).first()
        if genre:
            book = Book(**book_data)
            db.session.add(book)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    genre_book_data = [
        {"genre_book_id": 1, "book_id": 1, "genre_id": 1},
        {"genre_book_id": 2, "book_id": 1, "genre_id": 2},
        {"genre_book_id": 3, "book_id": 1, "genre_id": 5},
        {"genre_book_id": 4, "book_id": 2, "genre_id": 1},
        {"genre_book_id": 5, "book_id": 2, "genre_id": 2},
        {"genre_book_id": 6, "book_id": 2, "genre_id": 5},
        {"genre_book_id": 7, "book_id": 2, "genre_id": 7},
        {"genre_book_id": 8, "book_id": 3, "genre_id": 5},
        {"genre_book_id": 9, "book_id": 3, "genre_id": 6},
        {"genre_book_id": 10, "book_id": 3, "genre_id": 1},
        {"genre_book_id": 11, "book_id": 3, "genre_id": 2},
        {"genre_book_id": 12, "book_id": 4, "genre_id": 1},
        {"genre_book_id": 13, "book_id": 4, "genre_id": 7},
        {"genre_book_id": 14, "book_id": 5, "genre_id": 3},
        {"genre_book_id": 15, "book_id": 5, "genre_id": 6},
        {"genre_book_id": 16, "book_id": 6, "genre_id": 1},
        {"genre_book_id": 17, "book_id": 6, "genre_id": 5},
        {"genre_book_id": 18, "book_id": 6, "genre_id": 3},
        {"genre_book_id": 19, "book_id": 6, "genre_id": 4}
    ]

    for data in genre_book_data:
        genre_book = GenreBook(**data)
        db.session.add(genre_book)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        initializer_book_context()
