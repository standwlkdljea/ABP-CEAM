from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.utils.db import Base, SessionLocal


class Doctor(Base):
    __tablename__ = 'doctores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_doctor = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    servicio_id = Column(Integer, ForeignKey('servicios.id'), nullable=False)
    estado = Column(Enum('activo', 'inactivo'), default='activo')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    @staticmethod
    def get_by_id(doctor_id):
        db = SessionLocal()
        try:
            return db.query(Doctor).filter(Doctor.id == doctor_id).first()
        finally:
            db.close()

    @staticmethod
    def get_by_email(email):
        db = SessionLocal()
        try:
            return db.query(Doctor).filter(Doctor.email == email).first()
        finally:
            db.close()

    @staticmethod
    def get_all_active():
        db = SessionLocal()
        try:
            return db.query(Doctor).filter(Doctor.estado == 'activo').all()
        finally:
            db.close()

    @staticmethod
    def get_by_servicio(servicio_id):
        db = SessionLocal()
        try:
            return db.query(Doctor).filter(
                Doctor.servicio_id == servicio_id,
                Doctor.estado == 'activo'
            ).all()
        finally:
            db.close()

    @staticmethod
    def set_estado(doctor_id, estado):
        db = SessionLocal()
        try:
            db.query(Doctor).filter(Doctor.id == doctor_id).update({Doctor.estado: estado})
            db.commit()
        finally:
            db.close()
