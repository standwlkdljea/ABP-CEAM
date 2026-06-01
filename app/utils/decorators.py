from functools import wraps
from flask import abort
from flask_login import current_user


def client_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'cliente':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def doctor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'doctor':
            abort(403)
        return f(*args, **kwargs)
    return decorated
