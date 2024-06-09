from flask import Blueprint, render_template,redirect, request, url_for, flash
from flask_login import login_required, current_user
from datetime import date

# Utils
from app.utils.url_safer import *
from app.utils.mapper import *

# Services
from app.services import reservation_service
from app.services import book_service

admin_reservation_bp = Blueprint("admin_reservation", __name__, template_folder="../../templates/admin/reservation")


@admin_reservation_bp.route("/", methods=["POST", "GET"])
def reservation_adm():
    return render_template("reservation-adm.html", active_page='reservation', reservations='reservations')

