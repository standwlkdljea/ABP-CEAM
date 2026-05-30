from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.utils.db import Base, SessionLocal


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    dni = Column(String(20), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(20))
    rol = Column(Enum('cliente', 'admin'), nullable=False, default='cliente')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    @staticmethod
    def get_by_id(user_id):
        db = SessionLocal()
        try:
            return db.query(Usuario).filter(Usuario.id == user_id).first()
        finally:
            db.close()

    @staticmethod
    def get_by_email(email):
        db = SessionLocal()
        try:
            return db.query(Usuario).filter(Usuario.email == email).first()
        finally:
            db.close()

    @staticmethod
    def get_by_dni(dni):
        db = SessionLocal()
        try:
            return db.query(Usuario).filter(Usuario.dni == dni).first()
        finally:
            db.close()

    @staticmethod
    def create(nombre_completo, dni, email, password_hash, telefono=None, rol='cliente'):
        db = SessionLocal()
        try:
            user = Usuario(
                nombre_completo=nombre_completo,
                dni=dni,
                email=email,
                password_hash=password_hash,
                telefono=telefono,
                rol=rol
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id
        finally:
            db.close()

    @staticmethod
    def get_all(search=None):
        db = SessionLocal()
        try:
            q = db.query(Usuario)
            if search:
                q = q.filter(
                    (Usuario.nombre_completo.like(f'%{search}%')) |
                    (Usuario.dni.like(f'%{search}%'))
                )
            return q.order_by(Usuario.created_at.desc()).all()
        finally:
            db.close()

    @staticmethod
    def delete(user_id):
        db = SessionLocal()
        try:
            db.query(Usuario).filter(Usuario.id == user_id).delete()
            db.commit()
        finally:
            db.close()
