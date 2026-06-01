from app.models.doctor import Doctor


class DoctorService:

    @staticmethod
    def get_doctores_disponibles():
        return Doctor.get_all_active()

    @staticmethod
    def get_doctores_por_servicio(servicio_id):
        return Doctor.get_by_servicio(servicio_id)

    @staticmethod
    def set_estado(doctor_id, estado):
        Doctor.set_estado(doctor_id, estado)
        return True
