from app import db
from sqlalchemy.orm import relationship

class Book(db.Model):

    __tablename__ = "book"

    id = db.Column("id", db.Integer, primary_key=True)
    isbn = db.Column("isbn", db.String(13), nullable=False, unique=True)
    title = db.Column("title", db.String(45), nullable=False)
    author = db.Column("author", db.String(45), nullable=False)
    publisher = db.Column("publisher", db.String(45), nullable=False)
    year = db.Column("year", db.String(5), nullable=False)
    totalStock = db.Column(db.Integer, nullable=False)
    availableStock = db.Column(db.Integer, nullable=False)
    isAvailable = db.Column(db.Boolean, nullable=False, default=True)

    # reservation relation
    reservations = relationship("Reservation", back_populates="book")

    # genre book relation
    genreBook = relationship("GenreBook", back_populates="book")

    def __init__(self, isbn, title, author, publisher, year, totalStock, availableStock):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year
        self.totalStock = totalStock
        self.availableStock = availableStock

        if self.availableStock > 0:
            self.isAvailable = True
        else:
            self.isAvailable = False

    def decreaseAvailableStock(self):
        if self.availableStock > 0:
            self.availableStock -= 1

    def increaseAvailableStock(self):
        if self.availableStock < self.totalStock:
            self.availableStock += 1

    def updateIsAvailable(self):
        if self.availableStock > 0:
            self.isAvailable = True
        else:
            self.isAvailable = False

    def __repr__(self):
        return f"<Book {self.title} by {self.author} (ISBN: {self.isbn}, Publisher: {self.publisher}, Year: {self.year}>"