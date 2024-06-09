from app.utils.url_safer import encode_id

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
        temp_reservation = {
            "id": encode_id(reservation.id),
            "status": reservation.status,
            "expirationDate": reservation.expirationDate,
            "renewCount": reservation.renewCount,
            "devolutionDate": reservation.devolutionDate,
            "book": reservation.book,
            "user": reservation.user
        }

        return temp_reservation

def userMapper(user):
    temp_user = {
        "id": encode_id(user.id),
        "name": user.name,
        "email": user.email,
        "cpf": user.cpf,
        "password_hash": user.password_hash,
        "isAdmin": user.isAdmin,
        "phonenumber": user.phonenumber
    }

    return temp_user