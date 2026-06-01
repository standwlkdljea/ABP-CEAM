from sqlalchemy import Column, Integer, String, SmallInteger, Text
from app.utils.db import Base, SessionLocal


class Servicio(Base):
    __tablename__ = 'servicios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    duracion_minutos = Column(SmallInteger, nullable=False)
    descripcion = Column(Text)

    @staticmethod
    def get_all():
        db = SessionLocal()
        try:
            return db.query(Servicio).all()
        finally:
            db.close()

    @staticmethod
    def get_by_id(servicio_id):
        db = SessionLocal()
        try:
            return db.query(Servicio).filter(Servicio.id == servicio_id).first()
        finally:
            db.close()
