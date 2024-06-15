from app import db
from sqlalchemy.orm import relationship

class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column("id", db.Integer, primary_key=True)
    genre_type = db.Column("genre_type", db.String(100), nullable=False)

    genreBook = relationship("GenreBook", back_populates="genre")

    def __init__(self, genre_type):
        self.genre_type = genre_type
