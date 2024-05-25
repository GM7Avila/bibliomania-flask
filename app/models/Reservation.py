from app import db
from sqlalchemy.orm import relationship
from Book import Book

class Reservation(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    reservationDate = db.Column(db.Date, nullable=False)
    expirationDate = db.Column(db.Date, nullable=False)
    devolutionDate = db.Column(db.Date)
    status = db.Column(db.String(100), nullable=False)
    renewCount = db.Column(db.Integer, default=0)

    # relacionamento com user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="reservations")

    # relacionamento com book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = relationship("Book", back_populates="reservations")

    def __init__(self, reservationDate, expirationDate, status, user_id, book_id):
        self.reservationDate = reservationDate
        self.expirationDate = expirationDate
        self.status = status
        self.user_id = user_id
        self.book_id = book_id
