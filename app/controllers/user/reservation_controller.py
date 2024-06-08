from flask import Blueprint, render_template,redirect, request, url_for, flash
from flask_login import login_required, current_user
from datetime import date

# Utils
from app.utils.url_safer import *
from app.utils.mapper import *

# Services
from app.services import reservation_service
from app.services import book_service

reservation_bp = Blueprint("reservation", __name__, template_folder="../../templates/client/reservation")

@reservation_bp.route("/", methods=["POST", "GET"])
@login_required
def reservation():
    reservations = []
    temp_reservations = []

    if request.method == "POST":
        search = request.form.get("input-search")

        filtro_selecionado = request.form.get("filtro")
        filtro_status = request.form.get("filtro-status")

        if filtro_status in ["Ativa", "Finalizada", "Atrasada"]:
            reservations = reservation_service.getUserReservationsByStatus(user_id=current_user.id, status=filtro_status)

        elif filtro_selecionado == "filtroISBN":
            reservations = reservation_service.getUserReservationsByBookISBN(user_id=current_user.id, isbn=search)
            print(reservations)

        elif filtro_selecionado == "filtroTitulo":
            books = book_service.getBooksBySimilarTitle(search)
            if books:
                reservations = reservation_service.getUserReservationsByBooks(user_id=current_user.id, books=books)

        elif filtro_selecionado == "filtroTodos":
            if search:
                reservations = reservation_service.getGlobalSearch(user_id=current_user.id, query=search)
            else:
                reservations = reservation_service.getReservationsByUser(user_id=current_user.id)

    if request.method == "GET":
        reservations = reservation_service.getReservationsByUser(user_id=current_user.id)

    for reservation in reservations:
        temp_reservations.append(reservationMapper(reservation))

    return render_template("reservation-list.html", active_page='reservation', reservations=temp_reservations)


@reservation_bp.route("/r=<token>", methods=["GET", "POST"])
@login_required
def reservation_detail(token):

    reservation_id = decode_id(token)

    print(reservation_id)

    reservation = reservation_service.getReservationById(reservation_id)

    if reservation is None:
        return redirect(url_for("reservation.reservation"))

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