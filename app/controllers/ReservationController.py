from app import db
from ..models.Reservation import Reservation
from datetime import date, timedelta
class ReservationController:

    """
    FUNÇÕES DE RENOVAÇÃO E DEVOLUÇÃO
    """
    @staticmethod
    def updateStatus(reservation_id):
        try:
            reservation = Reservation.query.get(reservation_id)

            if reservation.expirationDate < date.today():
                reservation.status = "Atrasada"

            if reservation.expirationDate >= date.today():
                reservation.status = "Ativa"

            if reservation.devolutionDate != None:
                reservation.status = "Finalizada"

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def renewReservation(reservation):
        try:
            #reservation = Reservation.query.get(reservation_id)
            if reservation.renewCount >= 4:
                return False

            reservation.expirationDate += timedelta(days=7)
            reservation.renewCount += 1
            db.session.commit()

            return True

        except Exception as e:
            db.session.rollback()
            return False

    @staticmethod
    def finishReservation(self, reservation):
        reservation.devolutionDate = date.today()

        if reservation.expirationDate < date.today():
            reservation.status = "Atrasada"
            return False

        reservation.status = "Finalizada"

        # atualiza o status do livro
        book = reservation.book
        book.increaseAvailableStock()
        book.updateIsAvailable()

        db.session.add(reservation)
        db.session.add(book)
        db.session.commit()

        return True # sem multa

    """
    FUNÇÕES BÁSICAS
    """
    # TODO - adm view: findUserByCpf (return user)
    @staticmethod
    def createReservation(user, book):
        try:
            if book.availableStock > 0:

                # faz a reserva e decrementa o valor
                reservation = Reservation(user.id, book.id)
                book.decreaseAvailableStock()

                # atualiza o status do livro
                book.updateIsAvailable()

                # salva no banco
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

    # reservas pelo ISBN (geral)
    @staticmethod
    def getReservationsByBookISBN(isbn):
        try:
            reservations = Reservation.query.filter(Reservation.book.has(isbn=isbn)).all()
            return reservations
        except Exception as e:
            return None

    # reservas pelo ISBN do usuario
    @staticmethod
    def getUserReservationsByBookISBN(user_id, isbn):
        try:
            reservations = Reservation.query.filter(Reservation.user_id == user_id).filter(
                Reservation.book.has(isbn=isbn)).all()
            return reservations
        except Exception as e:
            return None

    # reservas pelo titulo (geral)
    @staticmethod
    def getReservationsByBookTitle(title):
        try:
            reservations = Reservation.query.filter(Reservation.book.has(title=title)).all()
            return reservations
        except Exception as e:
            return None
    # reservas pelo titulo do usuario
    @staticmethod
    def getUserReservationsByBookTitle(user_id, title):
        try:
            reservations = Reservation.query.filter_by(user_id=user_id).filter(Reservation.book.has(title=title)).all()
            return reservations
        except Exception as e:
            return None

    # busca todsas as reservas de um status
    @staticmethod
    def getReservationsByStatus(status):
        try:
            reservations = Reservation.query.filter_by(status=status).all()
            return reservations
        except Exception as e:
            return None

    # busca todas as reservas de um usuário
    @staticmethod
    def getUserReservationsByStatus(user_id, status):
        try:
            reservations = Reservation.query.filter_by(user_id=user_id, status=status).all()
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

    @staticmethod
    def has_active_reservations(user_id):
        active_reservations = Reservation.query.filter_by(user_id=user_id, status="Ativa").first()
        return bool(active_reservations)

    @staticmethod
    def can_renew(reservation):
        try:
            return (
                reservation.status == "Ativa"
                and reservation.expirationDate >= date.today()
                and reservation.renewCount < 3
            )
        except Exception as e:
            return False