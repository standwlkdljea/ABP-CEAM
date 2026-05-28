from datetime import datetime, timedelta
from app.models import Doctor, Servicio, HorarioTrabajo, Configuracion, Cita
from app import db


def find_available_vet(service_id, start_time):
    """
    Returns (vet_obj, None) if a suitable vet is found,
    else (None, error_message).
    """
    # 1. Validate working hours
    day_of_week = start_time.weekday()  # Monday=0, Sunday=6
    wh = HorarioTrabajo.query.filter_by(dia_semana=day_of_week).first()
    if not wh:
        return None, "La clínica no abre ese día."

    # 2. Get service duration
    service = Servicio.query.get(service_id)
    if not service:
        return None, "Servicio no encontrado."
    end_time = start_time + timedelta(minutes=service.duracion_minutos)

    # 3. Check booking buffer before closing
    buffer_cfg = Configuracion.query.filter_by(clave="buffer_reserva_minutos").first()
    buffer_min = int(buffer_cfg.valor) if buffer_cfg else 60

    opening = datetime.combine(start_time.date(), wh.hora_apertura)
    closing = datetime.combine(start_time.date(), wh.hora_cierre) - timedelta(
        minutes=buffer_min
    )

    if not (opening <= start_time and end_time <= closing):
        return (
            None,
            "La cita debe caer completamente dentro del horario laboral y terminar al menos {} minutos antes del cierre.".format(
                buffer_min
            ),
        )

    # 4. Find free vets for this service
    vets = Doctor.query.filter_by(servicio_id=service_id, estado="libre").all()
    if not vets:
        return (
            None,
            "No hay veterinarios disponibles para este servicio en este momento.",
        )

    # 5. Check appointment overlap for each vet
    for vet in vets:
        conflict = Cita.query.filter(
            Cita.id_doctor == vet.id,
            Cita.estado == "programada",
            Cita.inicio < end_time,
            Cita.fin > start_time,
        ).first()
        if not conflict:
            return vet, None

    return (
        None,
        "Todos los veterinarios para este servicio están ocupados en ese horario.",
    )
