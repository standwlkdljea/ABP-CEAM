from datetime import datetime, timedelta
from app.models.horario import HorarioTrabajo
from app.models.configuracion import Configuracion


class HorarioService:

    @staticmethod
    def es_dia_laboral(fecha):
        dia_semana = fecha.weekday()
        horario = HorarioTrabajo.get_by_dia(dia_semana)
        return horario is not None

    @staticmethod
    def obtener_horario(fecha):
        dia_semana = fecha.weekday()
        return HorarioTrabajo.get_by_dia(dia_semana)

    @staticmethod
    def validar_cita_en_horario(inicio, duracion_minutos):
        fecha = inicio.date() if hasattr(inicio, 'date') else inicio
        if isinstance(inicio, str):
            inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M:%S')
            fecha = inicio.date()

        horario = HorarioService.obtener_horario(fecha)
        if not horario:
            return False, 'La clínica no abre ese día.'

        hora_apertura = horario.hora_apertura
        hora_cierre = horario.hora_cierre

        if isinstance(hora_apertura, timedelta):
            hora_apertura_dt = datetime.combine(fecha, datetime.min.time()) + hora_apertura
            hora_cierre_dt = datetime.combine(fecha, datetime.min.time()) + hora_cierre
        else:
            hora_apertura_dt = datetime.combine(fecha, hora_apertura)
            hora_cierre_dt = datetime.combine(fecha, hora_cierre)

        fin = inicio + timedelta(minutes=duracion_minutos)

        if inicio < hora_apertura_dt:
            return False, f'La clínica abre a las {hora_apertura}.'

        if fin > hora_cierre_dt:
            return False, f'La cita debe terminar antes del cierre ({hora_cierre}).'

        horas_antes_cierre = Configuracion.get('horas_antes_cierre_corte')
        if horas_antes_cierre:
            try:
                horas_antes = int(horas_antes_cierre)
            except ValueError:
                horas_antes = 1
        else:
            horas_antes = 1

        corte = hora_cierre_dt - timedelta(hours=horas_antes)
        if inicio > corte:
            return False, f'No se pueden agendar citas en la última hora antes del cierre.'

        return True, None
