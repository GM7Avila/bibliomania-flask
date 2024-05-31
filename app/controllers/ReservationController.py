from app import db
from ..models.Reservation import Reservation
import datetime

class ReservationController:

    """
    FUNÇÕES DE RENOVAÇÃO E DEVOLUÇÃO
    """
    @staticmethod
    def renewReservation(reservation):
        try:
            #reservation = Reservation.query.get(reservation_id)
            if reservation.renewCount > 3:
                return False

            reservation.expirationDate = datetime.date.today() + datetime.timedelta(days=7)
            reservation.renewCount += 1
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def finishReservation(reservation):
        reservation.status = "Finalizada"
        reservation.devolutionDate = datetime.date.today()

        book = reservation.book
        book.increaseAvailableStock()

        db.session.add(reservation)
        db.session.add(book)
        db.session.commit()

        if reservation.expirationDate < datetime.date.today():
            return False # gerar multa

        return True # sem multa

    """
    FUNÇÕES BÁSICAS
    """
    # TODO - adm view: findUserByCpf (return user)
    @staticmethod
    def createReservation(user, book):
        try:
            if book.availableStock > 0:
                reservation = Reservation(user.id, book.id)
                book.decreaseAvailableStock()

                db.session.add(reservation)
                db.session.add(book)

                db.session.commit()
                return reservation
        except Exception as e:
            db.session.rollback()
            return None

    # busca UMA reserva pelo próprio id
    @staticmethod
    def getReservationById(reservation_id):
        try:
            reservation = Reservation.query.get(reservation_id)
            return reservation
        except Exception as e:
            return None

    # TODO - adm view: findUserByCpf (return user) -> passar user_id
    @staticmethod
    def getReservationsByUser(user_id):
        try:
            reservations = Reservation.query.filter_by(user_id=user_id).all()
            return reservations
        except Exception as e:
            return None

    # pode buscar reservas passadas com o mesmo ISBN
    @staticmethod
    def getReservationsByISBN(isbn):
        try:
            reservations = Reservation.query.filter_by(isbn=isbn).all()
            return reservations
        except Exception as e:
            return None

    @staticmethod
    def getAllReservations():
        try:
            reservations = Reservation.query.all()
            return reservations
        except Exception as e:
            return None

    @staticmethod
    def getReservationsByBook(book_id):
        try:
            reservations = Reservation.query.filter_by(book_id=book_id).all()
            return reservations
        except Exception as e:
            return None

    @staticmethod
    def getReservationsByStatus(status):
        try:
            reservations = Reservation.query.filter_by(status=status).all()
            return reservations
        except Exception as e:
            return None

    @staticmethod
    def deleteReservation(reservation_id):
        try:
            reservation = Reservation.query.get(reservation_id)
            if reservation:
                db.session.delete(reservation)
                db.session.commit()
                return True
            else:
                return False
        except Exception as e:
            db.session.rollback()
            return False
