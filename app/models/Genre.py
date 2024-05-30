from app import db
from sqlalchemy.orm import relationship

class Genre(db.Model):
    __tablename__ = "genre"

    _id = db.Column("id", db.Integer, primary_key=True)
    type = db.Column('genre_type', db.String(100), nullable=False)

    genreBook = relationship("GenreBook", back_populates="genre")

    def __init__(self, type):
        self.type = type
