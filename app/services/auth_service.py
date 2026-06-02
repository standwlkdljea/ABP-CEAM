from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.models.doctor import Doctor


class AuthService:

    @staticmethod
    def register_cliente(nombre_completo, dni, email, password, telefono=None):
        existing = Usuario.get_by_email(email)
        if existing:
            return None, 'Ya existe una cuenta con ese correo electrónico.'

        existing_dni = Usuario.get_by_dni(dni)
        if existing_dni:
            return None, 'Ya existe una cuenta con ese DNI.'

        password_hash = generate_password_hash(password)
        user_id = Usuario.create(nombre_completo, dni, email, password_hash, telefono)
        user = Usuario.get_by_id(user_id)
        return user, None

    @staticmethod
    def authenticate_cliente(email, password):
        user = Usuario.get_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user, None
        return None, 'Correo o contraseña incorrectos.'

    @staticmethod
    def register_doctor(nombre_doctor, email, password, servicio_id):
        existing = Doctor.get_by_email(email)
        if existing:
            return None, 'Ya existe una cuenta de doctor con ese correo electrónico.'

        password_hash = generate_password_hash(password)
        doctor_id = Doctor.create(nombre_doctor, email, password_hash, servicio_id)
        doctor = Doctor.get_by_id(doctor_id)
        return doctor, None

    @staticmethod
    def authenticate_doctor(email, password):
        doctor = Doctor.get_by_email(email)
        if doctor and check_password_hash(doctor.password_hash, password):
            return doctor, None
        return None, 'Correo o contraseña incorrectos.'
