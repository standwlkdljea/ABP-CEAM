from sqlalchemy import Column, Integer, String
from app.utils.db import Base, SessionLocal


class Configuracion(Base):
    __tablename__ = 'configuraciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    clave = Column(String(50), nullable=False, unique=True)
    valor = Column(String(255), nullable=False)

    @staticmethod
    def get(clave):
        db = SessionLocal()
        try:
            row = db.query(Configuracion).filter(Configuracion.clave == clave).first()
            return row.valor if row else None
        finally:
            db.close()

    @staticmethod
    def get_all():
        db = SessionLocal()
        try:
            rows = db.query(Configuracion).all()
            return {row.clave: row.valor for row in rows}
        finally:
            db.close()
