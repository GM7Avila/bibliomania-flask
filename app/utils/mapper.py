from app.utils.url_safer import encode_id
from app.utils.format_mask import *

def bookMapper(book):
    temp_book = {
        "id": encode_id(book.id),
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "year": book.year,
        "totalStock": book.totalStock,
        "availableStock": book.availableStock,
        "isAvailable": book.isAvailable
    }

    return temp_book

def reservationMapper(reservation):

        user_mapper = userMapper(reservation.user)

        temp_reservation = {
            "id": encode_id(reservation.id),
            "status": reservation.status,
            "expirationDate": reservation.expirationDate,
            "reservationDate": reservation.reservationDate,
            "renewCount": reservation.renewCount,
            "devolutionDate": reservation.devolutionDate,
            "book": reservation.book,
            "user": user_mapper
        }

        return temp_reservation

def userMapper(user):

    phone_mask = format_phone_number(user.phonenumber)
    cpf_mask = format_cpf(user.cpf)

    temp_user = {
        "id": encode_id(user.id),
        "name": user.name,
        "email": user.email,
        "cpf": cpf_mask,
        "password_hash": user.password_hash,
        "isAdmin": user.isAdmin,
        "phonenumber": phone_mask
    }

    return temp_user