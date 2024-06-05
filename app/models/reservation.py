from app import db
from sqlalchemy.orm import relationship
from datetime import date, timedelta

class Reservation(db.Model):

    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True)
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

    def __init__(self, user_id, book_id):
        self.reservationDate = date.today()
        self.expirationDate = date.today() + timedelta(days=7)
        self.status = "Ativa"
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        if self.devolutionDate:
            return f"Reservation('{self.reservationDate}', '{self.expirationDate}', '{self.devolutionDate}', '{self.status}', '{self.user_id}', '{self.book_id}')"
        else:
            return f"Reservation('{self.reservationDate}', '{self.expirationDate}', None, '{self.status}', '{self.user_id}', '{self.book_id}')"
