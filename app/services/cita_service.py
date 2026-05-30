from datetime import datetime, timedelta
from app.models.cita import Cita
from app.models.doctor import Doctor
from app.models.servicio import Servicio
from app.services.horario_service import HorarioService


class CitaService:

    @staticmethod
    def agendar_cita(id_mascota, servicio_id, inicio_str, motivo):
        errors = []

        servicio = Servicio.get_by_id(servicio_id)
        if not servicio:
            return None, ['El servicio seleccionado no existe.']

        try:
            inicio = datetime.strptime(inicio_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            return None, ['Formato de fecha inválido.']

        if inicio < datetime.now():
            return None, ['No se pueden agendar citas en el pasado.']

        valido, error_horario = HorarioService.validar_cita_en_horario(inicio, servicio.duracion_minutos)
        if not valido:
            return None, [error_horario]

        fin = inicio + timedelta(minutes=servicio.duracion_minutos)

        doctores = Doctor.get_by_servicio(servicio_id)
        if not doctores:
            return None, ['No hay doctores disponibles para este servicio.']

        doctor_asignado = None
        for doctor in doctores:
            overlapping = Cita.get_overlapping(doctor.id, inicio, fin)
            if not overlapping:
                doctor_asignado = doctor
                break

        if not doctor_asignado:
            return None, ['No hay doctores disponibles en ese horario. Intente otra fecha u hora.']

        cita_id = Cita.create(inicio, motivo, servicio_id, id_mascota, doctor_asignado.id)
        return cita_id, None

    @staticmethod
    def get_citas_usuario(usuario_id):
        return Cita.get_by_usuario(usuario_id)

    @staticmethod
    def get_citas_doctor(doctor_id):
        return Cita.get_by_doctor(doctor_id)

    @staticmethod
    def cancelar_cita(cita_id):
        Cita.update_estado(cita_id, 'cancelada')
        return True

    @staticmethod
    def completar_cita(cita_id, doctor_id, observaciones=None, asistio=True):
        estado_historial = 'asistido' if asistio else 'no asistido'
        from app.models.historial import HistorialCita
        HistorialCita.create(cita_id, doctor_id, estado_historial, observaciones)
        nuevo_estado = 'completada' if asistio else 'cancelada'
        Cita.update_estado(cita_id, nuevo_estado)
        return True
