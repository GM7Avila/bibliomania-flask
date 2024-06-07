from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required, current_user
from datetime import date

# Services
from app.services import reservation_service
from app.services import book_service

reservation_bp = Blueprint("reservation", __name__, template_folder="../templates/client/reservation")

@reservation_bp.route("/", methods=["POST", "GET"])
@login_required
def reservation():

    if request.method == "POST":
        search = request.form.get("input-search")
        reservations = []

        filtro_selecionado = request.form.get("filtro")

        filtro_status = request.form.get("filtro-status")

        print(f"Filtro selecionado: {filtro_selecionado}")
        print(f"Texto de busca: {search}")


        if filtro_status == "Ativa":
            reservations = reservation_service.getUserReservationsByStatus(user_id=current_user.id, status=filtro_status)
            return render_template("reservation-list.html", active_page='reservation', reservations=reservations)
        if filtro_status == "Finalizada":
            reservations = reservation_service.getUserReservationsByStatus(user_id=current_user.id, status=filtro_status)
            return render_template("reservation-list.html", active_page='reservation', reservations=reservations)
        if filtro_status == "Atrasada":
            reservations = reservation_service.getUserReservationsByStatus(user_id=current_user.id, status=filtro_status)
            return render_template("reservation-list.html", active_page='reservation', reservations=reservations)
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

@reservation_bp.route("/<int:reservation_id>", methods=["GET", "POST"])
@login_required
def reservation_detail(reservation_id):

    reservation = reservation_service.getReservationById(reservation_id)

    if reservation is None:
        return render_template(url_for("reservation.list"))

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