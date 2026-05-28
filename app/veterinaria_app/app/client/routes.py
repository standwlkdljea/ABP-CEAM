from flask import render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models import Mascota, Servicio, Cita
from app.utils import find_available_vet
from . import client_blueprint


def client_required(func):
    """Decorator to restrict access to clients only."""
    from functools import wraps

    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if not hasattr(current_user, "role") or current_user.role != "client":
            return render_template("403.html"), 403
        return func(*args, **kwargs)

    return wrapper


@client_blueprint.route("/mascotas")
@client_required
def mascotas():
    pets = current_user.mascotas.all()
    return render_template("mascotas.html", pets=pets)


@client_blueprint.route("/citas")
@client_required
def citas():
    pets = current_user.mascotas.all()
    services = Servicio.query.all()
    return render_template("citas.html", pets=pets, services=services)


# API endpoints for pets
@client_blueprint.route("/api/pets", methods=["GET"])
@login_required
def get_pets():
    if current_user.role != "client":
        return jsonify({"error": "Unauthorized"}), 403
    pets = [
        {
            "id": p.id,
            "nombre_mascota": p.nombre_mascota,
            "tipo_mascota": p.tipo_mascota,
            "edad": p.edad,
            "descripcion": p.descripcion or "",
        }
        for p in current_user.mascotas.all()
    ]
    return jsonify(pets)


@client_blueprint.route("/api/pets", methods=["POST"])
@login_required
def add_pet():
    if current_user.role != "client":
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    required = ["nombre_mascota", "tipo_mascota", "edad"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    try:
        edad = int(data["edad"])
    except:
        return jsonify({"error": "Invalid age"}), 400
    pet = Mascota(  # type: ignore
        nombre_mascota=data["nombre_mascota"],
        tipo_mascota=data["tipo_mascota"],
        edad=edad,
        descripcion=data.get("descripcion", ""),
        id_usuario=current_user.id,
    )
    db.session.add(pet)
    db.session.commit()
    return jsonify({"id": pet.id, "message": "Pet created"}), 201


@client_blueprint.route("/api/pets/<int:pet_id>", methods=["DELETE"])
@login_required
def delete_pet(pet_id):
    if current_user.role != "client":
        return jsonify({"error": "Unauthorized"}), 403
    pet = Mascota.query.filter_by(id=pet_id, id_usuario=current_user.id).first()
    if not pet:
        return jsonify({"error": "Pet not found"}), 404
    db.session.delete(pet)
    db.session.commit()
    return jsonify({"message": "Pet deleted"}), 200


# Booking API
@client_blueprint.route("/api/citas", methods=["POST"])
@login_required
def book_appointment():
    if current_user.role != "client":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    required = ["pet_id", "service_id", "start_time", "motivo"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    try:
        pet = Mascota.query.filter_by(
            id=data["pet_id"], id_usuario=current_user.id
        ).first()
        if not pet:
            return jsonify(
                {"error": "Mascota no encontrada o no pertenece al usuario"}
            ), 400

        start_time = datetime.fromisoformat(data["start_time"])
        if start_time < datetime.now():
            return jsonify({"error": "No se pueden agendar citas en el pasado."}), 400

        vet, err = find_available_vet(data["service_id"], start_time)
        if vet is None:
            return jsonify({"error": err}), 400

        service = Servicio.query.get(data["service_id"])
        if not service:
            return jsonify({"error": "Servicio no encontrado"}), 400

        end_time = start_time + timedelta(minutes=service.duracion_minutos)

        new_cita = Cita(  # type: ignore
            inicio=start_time,
            fin=end_time,
            motivo=data["motivo"],
            servicio_id=data["service_id"],
            id_mascota=pet.id,
            id_doctor=vet.id,
            estado="programada",
        )
        db.session.add(new_cita)
        db.session.commit()
        return jsonify(
            {"message": "Cita agendada correctamente", "appointment_id": new_cita.id}
        ), 201
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
