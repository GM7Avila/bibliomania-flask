from app import db
from sqlalchemy.orm import relationship

class GenreBook(db.Model):
    __tablename__ = "genreBook"

    id = db.Column(db.Integer, primary_key=True, unique=True)

    # relacionamento com book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = relationship("Book", back_populates="genreBook")

    # relacionamento com genre
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = relationship("Genre", back_populates="genreBook")

    def __init__(self, genre_book_id, book_id, genre_id):
        self.id = genre_book_id
        self.book_id = book_id
        self.genre_id = genre_id

