from sqlalchemy import Column, Integer, Enum, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.utils.db import Base, SessionLocal


class HistorialCita(Base):
    __tablename__ = 'historial_citas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cita_id = Column(Integer, ForeignKey('citas.id', ondelete='CASCADE'), nullable=False, unique=True)
    doctor_id = Column(Integer, ForeignKey('doctores.id', ondelete='RESTRICT'), nullable=False)
    estado = Column(Enum('asistido', 'no asistido'), nullable=False)
    observaciones = Column(Text)
    fecha_validacion = Column(DateTime, server_default=func.current_timestamp())

    @staticmethod
    def create(cita_id, doctor_id, estado, observaciones=None):
        db = SessionLocal()
        try:
            hist = HistorialCita(
                cita_id=cita_id,
                doctor_id=doctor_id,
                estado=estado,
                observaciones=observaciones
            )
            db.add(hist)
            db.commit()
            db.refresh(hist)
            return hist.id
        finally:
            db.close()

    @staticmethod
    def get_by_cita(cita_id):
        db = SessionLocal()
        try:
            return db.query(HistorialCita).filter(HistorialCita.cita_id == cita_id).first()
        finally:
            db.close()
