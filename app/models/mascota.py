from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.utils.db import Base, SessionLocal


class Mascota(Base):
    __tablename__ = 'mascotas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_mascota = Column(String(50), nullable=False)
    tipo_mascota = Column(String(30), nullable=False)
    edad = Column(Integer, nullable=False)
    descripcion = Column(Text)
    id_usuario = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    @staticmethod
    def get_by_id(mascota_id):
        db = SessionLocal()
        try:
            return db.query(Mascota).filter(Mascota.id == mascota_id).first()
        finally:
            db.close()

    @staticmethod
    def get_by_usuario(usuario_id):
        db = SessionLocal()
        try:
            return db.query(Mascota).filter(
                Mascota.id_usuario == usuario_id
            ).order_by(Mascota.nombre_mascota).all()
        finally:
            db.close()

    @staticmethod
    def create(nombre_mascota, tipo_mascota, edad, id_usuario, descripcion=None):
        db = SessionLocal()
        try:
            mascota = Mascota(
                nombre_mascota=nombre_mascota,
                tipo_mascota=tipo_mascota,
                edad=edad,
                id_usuario=id_usuario,
                descripcion=descripcion
            )
            db.add(mascota)
            db.commit()
            db.refresh(mascota)
            return mascota.id
        finally:
            db.close()

    @staticmethod
    def delete(mascota_id):
        db = SessionLocal()
        try:
            db.query(Mascota).filter(Mascota.id == mascota_id).delete()
            db.commit()
        finally:
            db.close()
