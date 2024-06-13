from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user

# Utils
from app.utils.mapper import bookMapper, reservationMapper, userMapper
from app.utils.url_safer import encode_id, decode_id
from app.utils.format_mask import format_cpf

# Services
from app.services import reservation_service, user_service

admin_reservation_bp = Blueprint("admin_reservation", __name__, template_folder="../../templates/admin/reservation")

@admin_reservation_bp.route("/", methods=["POST", "GET"])
def reservation_adm():
    reservations = []
    temp_reservations = []

    if request.method == "POST":
        search = request.form.get("input-search")
        filtro_selecionado = request.form.get("filtro")
        filtro_status = request.form.get("filtro-status")

        if filtro_status in ["Ativa", "Finalizada", "Atrasada", "Em Espera", "Cancelada"]:
            reservations = reservation_service.getReservationsByStatus(status=filtro_status)
        elif filtro_selecionado == "filtroISBN":
            reservations = reservation_service.getReservationsByBookISBN(isbn=search)
        elif filtro_selecionado == "filtroCPF":
            search_digits = ''.join(filter(str.isdigit, search))
            print("CPF para busca (apenas dígitos):", search_digits)
            user = user_service.findUserByCPF(search_digits)
            if user:
                reservations = reservation_service.getReservationsByUser(user_id=user.id)
        elif filtro_selecionado == "filtroTodos":
            if search:
                reservations = reservation_service.getGlobalSearch(user_id=current_user.id, query=search)
            else:
                reservations = reservation_service.getAllReservations()

    if request.method == "GET":
        reservations = reservation_service.getAllReservations()

    for reservation in reservations:
        temp_reservations.append(reservationMapper(reservation))

    return render_template("reservation-adm.html", active_page='reservation', reservations=temp_reservations)

@admin_reservation_bp.route("/r=<token>", methods=["POST", "GET"])
def reservation_details(token):
    reservation_id = decode_id(token)
    reservation = reservation_service.getReservationById(reservation_id)

    if reservation is None:
        return redirect(url_for("admin_reservation.reservation_adm"))

    reservation_service.updateStatus(reservation_id)

    if request.method == "POST":
        if request.form.get("action") == "cancel" and reservation.status == "Em Espera":
            reservation_service.cancelReservation(reservation)

            flash("Reserva cancelada com sucesso!", "success")

        if request.form.get("action") == "active" and reservation.status == "Em Espera":
            success = reservation_service.updateReservationStatus(reservation, "Ativa")
            if success:
                flash("Reserva ativa com sucesso!", "success")
            else:
                flash("Erro ao ativar a reserva.", "error")

        if request.form.get("action") == "renew" and reservation_service.can_renew(reservation):
            success = reservation_service.renewReservation(reservation)
            if success:
                flash("Reserva renovada com sucesso!", "success")
            else:
                flash("Erro ao renovar a reserva.", "error")

        if request.form.get("action") == "finalize" and reservation.status == "Ativa" or reservation.status == "Atrasada":
            success = reservation_service.finishReservation(reservation)
            if success:
                flash("Reserva finalizada com sucesso!", "success")
            else:
                flash("Erro ao finalizar a reserva.", "error")

    can_renew = reservation_service.can_renew(reservation)
    reservation_mapped = reservationMapper(reservation)

    return render_template("adm-reservation-confirm.html", reservation=reservation_mapped, can_renew=can_renew)
