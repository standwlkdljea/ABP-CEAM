from flask import Flask
from flask_login import LoginManager
from app.config import SECRET_KEY
from app.models.usuario import Usuario
from app.models.doctor import Doctor


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta sección.'


class AppUser:
    def __init__(self, user_id, nombre, email, tipo, **kwargs):
        self.id = user_id
        self.nombre = nombre
        self.email = email
        self.tipo = tipo
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None

    if user_id.startswith('cliente_'):
        real_id = int(user_id.replace('cliente_', ''))
        row = Usuario.get_by_id(real_id)
        if row:
            return AppUser(
                user_id=user_id,
                nombre=row.nombre_completo,
                email=row.email,
                tipo='cliente',
                cliente_id=row.id,
                rol=row.rol,
                dni=row.dni,
                telefono=row.telefono
            )

    elif user_id.startswith('doctor_'):
        real_id = int(user_id.replace('doctor_', ''))
        row = Doctor.get_by_id(real_id)
        if row:
            return AppUser(
                user_id=user_id,
                nombre=row.nombre_doctor,
                email=row.email,
                tipo='doctor',
                doctor_id=row.id,
                servicio_id=row.servicio_id,
                estado=row.estado
            )

    return None


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    login_manager.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.doctor_routes import doctor_bp
    from app.routes.cita_routes import cita_bp
    from app.routes.mascota_routes import mascota_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(cita_bp)
    app.register_blueprint(mascota_bp)

    return app
