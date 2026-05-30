from sqlalchemy import Column, Integer, Time
from app.utils.db import Base, SessionLocal


class HorarioTrabajo(Base):
    __tablename__ = 'horarios_trabajo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dia_semana = Column(Integer, nullable=False, unique=True)
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)

    @staticmethod
    def get_all():
        db = SessionLocal()
        try:
            return db.query(HorarioTrabajo).order_by(HorarioTrabajo.dia_semana).all()
        finally:
            db.close()

    @staticmethod
    def get_by_dia(dia_semana):
        db = SessionLocal()
        try:
            return db.query(HorarioTrabajo).filter(HorarioTrabajo.dia_semana == dia_semana).first()
        finally:
            db.close()
