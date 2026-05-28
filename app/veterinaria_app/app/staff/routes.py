from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Cita
from . import staff_blueprint


def staff_required(func):
    from functools import wraps

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if not hasattr(current_user, "role") or current_user.role != "staff":
            return render_template("403.html"), 403
        return func(*args, **kwargs)

    return wrapper


@staff_blueprint.route("/dashboard")
@staff_required
def dashboard():
    # Upcoming scheduled appointments for this vet
    appointments = (
        Cita.query.filter_by(id_doctor=current_user.id, estado="programada")
        .order_by(Cita.inicio.asc())
        .all()
    )

    # Enrich with needed relations (mascota, owner, servicio)
    for appt in appointments:
        # Eager loading may help but for simplicity:
        _ = appt.mascota, appt.mascota.owner, appt.servicio

    return render_template("staff_dashboard.html", appointments=appointments)


@staff_blueprint.route("/toggle-status", methods=["POST"])
@staff_required
def toggle_status():
    if current_user.estado == "libre":
        current_user.estado = "ocupado"
    else:
        current_user.estado = "libre"
    db.session.commit()
    flash("Estado actualizado correctamente.")
    return redirect(url_for("staff.dashboard"))
