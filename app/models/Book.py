from app import db
from sqlalchemy.orm import relationship
from Reservation import Reservation

class Book(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    isbn = db.Column("isbn", db.String(13), nullable=False, unique=True)
    title = db.Column("title", db.String(45), nullable=False)
    author = db.Column("author", db.String(45), nullable=False)
    publisher = db.Column("publisher", db.String(45), nullable=False)
    year = db.Column("year", db.String(5), nullable=False)
    totalStock = db.Column(db.Integer, nullable=False)
    availableStock = db.Column(db.Integer, nullable=False)

    # reservation relation
    reservation = relationship("Reservation", back_populates="Book")

    def __init__(self, isbn, title, author, publisher, year, totalStock, availableStock):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.totalStock = totalStock
        self.availableStock = availableStock