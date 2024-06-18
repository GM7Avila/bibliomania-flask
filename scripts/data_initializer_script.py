import sys
import os
import uuid

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
    # Verifica se o admin já existe
    admin = User.query.filter_by(email="admin@bibliomania").first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@bibliomania",
            cpf=11111111111,
            password="admin",
            isAdmin=True,
            phonenumber="11111111111"
        )
        db.session.add(admin)
        db.session.commit()

    users_data = [
        {
            "name": "Guilherme Avila",
            "email": "guilherme@gmail.com",
            "cpf": 12133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "24998232712"
        },
        {
            "name": "Lucia Pereira",
            "email": "lucia_pereira@gmail.com",
            "cpf": 81133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21878232712"
        },
        {
            "name": "Ana Clara de Souza",
            "email": "ana_clara@hotmail.com",
            "cpf": 91133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21878232712"
        },
        {
            "name": "Luiz Eduardo França",
            "email": "luiz_eduardo@gmail.com",
            "cpf": 71123456352,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21978832719"
        },
        {
            "name": "Fernanda Oliveira",
            "email": "fernanda.oliveira@example.com",
            "cpf": 52133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21998877665"
        },
        {
            "name": "Rafael Silva",
            "email": "rafael.silva@example.com",
            "cpf": 62133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21887766554"
        },
        {
            "name": "Marina Santos",
            "email": "marina.santos@example.com",
            "cpf": 72133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21336655443"
        },
        {
            "name": "Pedro Almeida",
            "email": "pedro.almeida@example.com",
            "cpf": 82133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21995544332"
        },
        {
            "name": "Carolina Pereira",
            "email": "carolina.pereira@example.com",
            "cpf": 92133456321,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21443322111"
        },
        {
            "name": "José Santos",
            "email": "jose.santos@example.com",
            "cpf": 10213345632,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21994433221"
        },
        {
            "name": "Juliana Souza",
            "email": "juliana.souza@example.com",
            "cpf": 11213445633,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21882211344"
        },
        {
            "name": "Marcos Lima",
            "email": "marcos.lima@example.com",
            "cpf": 12213545634,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21776655455"
        },
        {
            "name": "Aline Oliveira",
            "email": "aline.oliveira@example.com",
            "cpf": 13213645635,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21334455666"
        },
        {
            "name": "Carlos Silva",
            "email": "carlos.silva@example.com",
            "cpf": 14213745636,
            "password": "senha",
            "isAdmin": False,
            "phonenumber": "21998877665"
        }
    ]

    for user_data in users_data:
        user = User.query.filter_by(email=user_data["email"]).first()
        if not user:
            user = User(**user_data)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    genres_data = [
        {"genre_type": "Fantasia"},
        {"genre_type": "Aventura"},
        {"genre_type": "Romance"},
        {"genre_type": "Ficção Científica"},
        {"genre_type": "Mistério"},
        {"genre_type": "Suspense"}
    ]

    for genre_data in genres_data:
        genre = Genre.query.filter_by(genre_type=genre_data["genre_type"]).first()
        if not genre:
            genre = Genre(**genre_data)
            db.session.add(genre)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

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
            "description": "As Voldemort's return becomes undeniable, Harry Potter finds himself isolated and discredited by the wizarding community. Forming 'Dumbledore's Army,' Harry and his friends prepare for the inevitable war while facing off against the authoritarian new headmistress, Dolores Umbridge. This year brings new trials, losses, and the unyielding fight for justice and truth."
        },
        {
            "isbn": "6780439372594",
            "title": "Harry Potter and the Half-Blood Prince",
            "author": "J. K. Rowling",
            "publisher": "Scholastic",
            "year": "2009",
            "totalStock": 18,
            "availableStock": 18,
            "genre_type": "Fantasia",
            "description": "With the wizarding world at war, Harry Potter's sixth year at Hogwarts is marked by danger and discovery. Guided by Dumbledore, Harry learns about Voldemort's past and the secret to defeating him. The Half-Blood Prince's mysterious textbook reveals new spells and potions, adding to the tension as friendships are tested and loyalties are questioned."
        }
    ]

    for book_data in books_data:
        book = Book.query.filter_by(isbn=book_data["isbn"]).first()
        if not book:
            book = Book(
                isbn=book_data["isbn"],
                title=book_data["title"],
                author=book_data["author"],
                publisher=book_data["publisher"],
                year=book_data["year"],
                totalStock=book_data["totalStock"],
                availableStock=book_data["availableStock"],
                description=book_data["description"]
            )
            db.session.add(book)
            db.session.commit()

            for genre_type in book_data["genres"]:
                genre = Genre.query.filter_by(genre_type=genre_type).first()
                if genre:
                    genre_book = GenreBook(
                        genre_id=genre.id,
                        book_id=book.id,
                        genre_book_id=uuid.uuid4().hex
                    )
                    db.session.add(genre_book)
                    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        initializer_book_context()
