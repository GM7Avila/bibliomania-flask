from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# Services / Models
from app.services.reservation_service import reservation_service
from app.services.book_service import book_service

res_bp = Blueprint("reservation", __name__, template_folder="templates")

@res_bp.route("/reservation", methods=["POST", "GET"])
@login_required
def reservation():

    if request.method == "POST":
        search = request.form.get("input-search")
        reservations = []

        filtro_selecionado = request.form.get("filtro")

        print(f"Filtro selecionado: {filtro_selecionado}")
        print(f"Texto de busca: {search}")

        if filtro_selecionado == "filtroStatus":
            reservations = reservation_service.getUserReservationsByStatus(user_id=current_user.id, status=search)
            print("1. STATUS selecionado")
            print("- Buscando por: " + search + "...")
            print(reservations)


        elif filtro_selecionado == "filtroISBN":
            reservations = reservation_service.getUserReservationsByBookISBN(user_id=current_user.id, isbn=search)
            print("1. ISBN selecionado")
            print("- Buscando por: " + search + "...")
            print(reservations)


        elif filtro_selecionado == "filtroTitulo":
            books = book_service.getBooksBySimilarTitle(search)
            if books:
                reservations = reservation_service.getUserReservationsByBooks(user_id=current_user.id, books=books)
                print("1. TITULO selecionado")
                print("- Buscando por: " + search + "...")
                print(reservations)
            else:
                print("Nenhum livro encontrado com o título: " + search)

        elif filtro_selecionado == "filtroTodos":
            print("1. ALL selecionado")
            print("- Buscando por: " + search + "...")
            if search:
                books = book_service.getBooksBySimilarTitle(search)
                reservations = reservation_service.getGlobalSearch(user_id=current_user.id, query=search, books=books)
                print(reservations)

            else:
                reservations = reservation_service.getReservationsByUser(user_id=current_user.id)
                print(reservations)

        return render_template("reservation-list.html", active_page='reservation', reservations=reservations)

    if request.method == "GET":
        reservations = reservation_service.getReservationsByUser(user_id=current_user.id)
        return render_template("reservation-list.html", active_page='reservation', reservations=reservations)

@res_bp.route("/reservation/<int:reservation_id>", methods=["GET", "POST"])
@login_required
def reservation_detail(reservation_id):

    reservation = reservation_service.getReservationById(reservation_id)

    if reservation is None:
        return render_template(url_for("reservation"))

    reservation_service.updateStatus(reservation_id)

    if request.method == "POST":
        if request.form.get("action") == "renew":
            if reservation.status == "Ativa" and reservation.expirationDate >= date.today() and reservation.renewCount < 3:
                success = reservation_service.renewReservation(reservation)
                if success:
                    flash("Reserva renovada com sucesso!", "success")
                else:
                    flash("Erro ao renovar a reserva.", "error")
            else:
                flash("Não é possível renovar a reserva. A reserva está atrasada ou finalizada.", "error")
        return render_template("reservation-details.html", reservation=reservation)

    can_renew = reservation_service.can_renew(reservation)

    return render_template("reservation-details.html", reservation=reservation, can_renew=can_renew)

@res_bp.route("/acervo/<int:book_id>", methods=["POST", "GET"])
def reservation_confirm(book_id):
    book = book_service.findBookById(book_id)
    user_id = current_user.id
    can_reserve = not reservation_service.has_active_reservations(user_id)
    return render_template("reservation-confirm.html", book=book,can_reserve=can_reserve)

@res_bp.route("/reservar/<int:book_id>", methods=["POST"])
def reservar(book_id):
    book = book_service.findBookById(book_id)
    user_id = current_user.id

    if reservation_service.has_active_reservations(user_id):
        flash("Você já possui reservas ativas. Não é possível fazer uma nova reserva.", "danger")
    else:
        reservation = reservation_service.createReservation(current_user, book)
        if reservation:
            flash("Reserva realizada com sucesso!", "success")
        else:
            flash("Não foi possível realizar a reserva. Tente novamente.", "danger")
    return redirect(url_for("acervo"))