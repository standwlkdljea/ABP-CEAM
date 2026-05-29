from app import db
from flask_login import UserMixin
from datetime import datetime


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mascotas = db.relationship(
        "Mascota", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )

    def get_id(self):
        return f"client-{self.id}"

    @property
    def role(self):
        return "client"

    # Flask-Login needs these properties; the UserMixin already provides is_authenticated etc.
    # We'll override is_active? No.


class Servicio(db.Model):
    __tablename__ = "servicios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    duracion_minutos = db.Column(db.SmallInteger, nullable=False)
    descripcion = db.Column(db.Text)


class Doctor(UserMixin, db.Model):
    __tablename__ = "doctores"
    id = db.Column(db.Integer, primary_key=True)
    nombre_doctor = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    estado = db.Column(db.Enum("libre", "ocupado"), default="libre")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    servicio = db.relationship("Servicio", backref="doctores")

    def get_id(self):
        return f"staff-{self.id}"

    @property
    def role(self):
        return "staff"


    


class Mascota(db.Model):
    __tablename__ = "mascotas"
    id = db.Column(db.Integer, primary_key=True)
    nombre_mascota = db.Column(db.String(50), nullable=False)
    tipo_mascota = db.Column(db.String(30), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)


class Cita(db.Model):
    __tablename__ = "citas"
    id = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)
    fin = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id"), nullable=False)
    id_mascota = db.Column(db.Integer, db.ForeignKey("mascotas.id"), nullable=False)
    id_doctor = db.Column(db.Integer, db.ForeignKey("doctores.id"), nullable=False)
    estado = db.Column(
        db.Enum("programada", "completada", "cancelada"), default="programada"
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mascota = db.relationship("Mascota", backref="citas")
    doctor = db.relationship("Doctor", backref="citas")
    servicio = db.relationship("Servicio")


class HorarioTrabajo(db.Model):
    __tablename__ = "horarios_trabajo"
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.SmallInteger, unique=True, nullable=False)
    hora_apertura = db.Column(db.Time, nullable=False)
    hora_cierre = db.Column(db.Time, nullable=False)


class Configuracion(db.Model):
    __tablename__ = "configuraciones"
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(255), nullable=False)
