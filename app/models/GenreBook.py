from app import db
from sqlalchemy.orm import relationship

class GenreBook(db.Model):
    __tablename__ = "genreBook"

    id = db.Column(db.Integer, primary_key=True)

    # relacionamento com book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = relationship("Book", back_populates="genreBook")

    # relacionamento com genre
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = relationship("Genre", back_populates="genreBook")