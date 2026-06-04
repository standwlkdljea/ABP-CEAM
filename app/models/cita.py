from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Enum, TIMESTAMP, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.db import Base, SessionLocal


class Cita(Base):
    __tablename__ = 'citas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    inicio = Column(DateTime, nullable=False)
    motivo = Column(Text, nullable=False)
    servicio_id = Column(Integer, ForeignKey('servicios.id', ondelete='RESTRICT'), nullable=False)
    id_mascota = Column(Integer, ForeignKey('mascotas.id', ondelete='CASCADE'), nullable=False)
    id_doctor = Column(Integer, ForeignKey('doctores.id', ondelete='RESTRICT'), nullable=False)
    estado = Column(Enum('programada', 'completada', 'cancelada'), default='programada')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    mascota = relationship('Mascota', lazy='joined')
    doctor = relationship('Doctor', lazy='joined')
    servicio = relationship('Servicio', lazy='joined')

    @property
    def nombre_mascota(self):
        return self.mascota.nombre_mascota if self.mascota else None

    @property
    def tipo_mascota(self):
        return self.mascota.tipo_mascota if self.mascota else None

    @property
    def nombre_doctor(self):
        return self.doctor.nombre_doctor if self.doctor else None

    @property
    def nombre_servicio(self):
        return self.servicio.nombre if self.servicio else None

    @staticmethod
    def get_by_id(cita_id):
        db = SessionLocal()
        try:
            return db.query(Cita).filter(Cita.id == cita_id).first()
        finally:
            db.close()

    @staticmethod
    def get_by_usuario(usuario_id):
        db = SessionLocal()
        try:
            from app.models.mascota import Mascota
            return db.query(Cita).join(Mascota, Cita.id_mascota == Mascota.id).filter(
                Mascota.id_usuario == usuario_id
            ).order_by(Cita.inicio.desc()).all()
        finally:
            db.close()

    @staticmethod
    def get_by_doctor(doctor_id):
        db = SessionLocal()
        try:
            return db.query(Cita).filter(
                Cita.id_doctor == doctor_id
            ).order_by(Cita.inicio.desc()).all()
        finally:
            db.close()

    GAP_MINUTOS = 20

    @staticmethod
    def get_overlapping(doctor_id, inicio, fin):
        db = SessionLocal()
        try:
            citas = db.query(Cita).filter(
                Cita.id_doctor == doctor_id,
                Cita.estado == 'programada'
            ).all()
            gap = timedelta(minutes=Cita.GAP_MINUTOS)
            overlapping = []
            for c in citas:
                c_fin = c.inicio + timedelta(minutes=c.servicio.duracion_minutos)
                if c.inicio < fin + gap and c_fin + gap > inicio:
                    overlapping.append(c)
            return overlapping
        finally:
            db.close()

    @staticmethod
    def create(inicio, motivo, servicio_id, id_mascota, id_doctor):
        db = SessionLocal()
        try:
            if isinstance(inicio, str):
                inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M:%S')
            cita = Cita(
                inicio=inicio,
                motivo=motivo,
                servicio_id=servicio_id,
                id_mascota=id_mascota,
                id_doctor=id_doctor
            )
            db.add(cita)
            db.commit()
            db.refresh(cita)
            return cita.id
        finally:
            db.close()

    @staticmethod
    def update_estado(cita_id, estado):
        db = SessionLocal()
        try:
            db.query(Cita).filter(Cita.id == cita_id).update({Cita.estado: estado})
            db.commit()
        finally:
            db.close()
