from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from datetime import date

# Utils
from app.utils.url_safer import *
from app.utils.mapper import *

# Services
from app.services import reservation_service
from app.services import book_service
from app.services import user_service

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
            print(reservations)
        elif filtro_selecionado == "filtroISBN":
            reservations = reservation_service.getReservationsByBookISBN(isbn=search)
        elif filtro_selecionado == "filtroCPF":
            user = user_service.findUserByCPF(cpf=search)
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

    print(temp_reservations)

    return render_template("reservation-adm.html", active_page='reservation', reservations=temp_reservations)
