from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login_client"  # type: ignore
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth_blueprint
    from app.client.routes import client_blueprint
    from app.staff.routes import staff_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(staff_blueprint, url_prefix="/staff")

    @login_manager.user_loader
    def load_user(user_id):
        # user_id format: 'client-123' or 'staff-456'
        if not user_id or "-" not in user_id:
            return None
        role, id_str = user_id.split("-", 1)
        id_int = int(id_str)
        if role == "client":
            return Usuario.query.get(id_int)
        elif role == "staff":
            return Doctor.query.get(id_int)
        return None

    # Make `current_user` available in templates as a dict‑like object.
    @app.context_processor
    def inject_user():
        from flask_login import current_user

        return dict(current_user=current_user)

    return app


# Import models here to avoid circular imports
from app.models import (
    Usuario,
    Doctor,
    Servicio,
    Mascota,
    Cita,
    HorarioTrabajo,
    Configuracion,
)
