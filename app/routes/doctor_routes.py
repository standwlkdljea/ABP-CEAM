from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import AppUser
from app.services.auth_service import AuthService
from app.services.doctor_service import DoctorService
from app.services.cita_service import CitaService
from app.models.servicio import Servicio
from app.utils.decorators import doctor_required


doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')


@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.tipo == 'doctor':
        return redirect(url_for('doctor.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        pwd = request.form.get('password', '')

        doctor_row, error = AuthService.authenticate_doctor(email, pwd)
        if error:
            flash(error, 'error')
            return render_template('doctor/login.html')

        doctor_user = AppUser(
            f'doctor_{doctor_row.id}',
            doctor_row.nombre_doctor, doctor_row.email, 'doctor',
            doctor_id=doctor_row.id, servicio_id=doctor_row.servicio_id,
            estado=doctor_row.estado
        )
        login_user(doctor_user)
        flash(f'¡Bienvenido/a, Dr/a. {doctor_row.nombre_doctor}!', 'success')
        return redirect(url_for('doctor.dashboard'))

    return render_template('doctor/login.html')


@doctor_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.tipo == 'doctor':
        return redirect(url_for('doctor.dashboard'))

    servicios = Servicio.get_all()

    if request.method == 'POST':
        nombre = request.form.get('nombre_doctor', '').strip()
        email = request.form.get('email', '').strip().lower()
        pwd = request.form.get('password', '')
        pwd2 = request.form.get('password2', '')
        servicio_id = request.form.get('servicio_id', '')

        error = None
        if not nombre or not email or not pwd or not servicio_id:
            error = 'Todos los campos son obligatorios.'
        elif pwd != pwd2:
            error = 'Las contraseñas no coinciden.'
        elif len(pwd) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'

        if error:
            flash(error, 'error')
            return render_template('doctor/register.html', servicios=servicios)

        doctor_row, error = AuthService.register_doctor(
            nombre, email, pwd, int(servicio_id)
        )
        if error:
            flash(error, 'error')
            return render_template('doctor/register.html', servicios=servicios)

        doctor_user = AppUser(
            f'doctor_{doctor_row.id}',
            doctor_row.nombre_doctor, doctor_row.email, 'doctor',
            doctor_id=doctor_row.id, servicio_id=doctor_row.servicio_id,
            estado=doctor_row.estado
        )
        login_user(doctor_user)
        flash(f'¡Bienvenido/a, Dr/a. {nombre}! Tu cuenta ha sido creada.', 'success')
        return redirect(url_for('doctor.dashboard'))

    return render_template('doctor/register.html', servicios=servicios)


@doctor_bp.route('/logout')
@doctor_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('main.home'))


@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    citas = CitaService.get_citas_doctor(current_user.doctor_id)
    return render_template('doctor/dashboard.html', citas=citas)


@doctor_bp.route('/toggle-status', methods=['POST'])
@doctor_required
def toggle_status():
    nuevo_estado = 'inactivo' if current_user.estado == 'activo' else 'activo'
    DoctorService.set_estado(current_user.doctor_id, nuevo_estado)
    current_user.estado = nuevo_estado
    label = 'disponible' if nuevo_estado == 'activo' else 'no disponible'
    flash(f'Tu estado ha cambiado a: {label}.', 'success')
    return redirect(url_for('doctor.dashboard'))


@doctor_bp.route('/cita/<int:cita_id>/completar', methods=['POST'])
@doctor_required
def completar_cita(cita_id):
    observaciones = request.form.get('observaciones', '').strip() or None
    asistio = request.form.get('asistio') == 'si'
    CitaService.completar_cita(cita_id, current_user.doctor_id, observaciones, asistio)
    flash('Cita actualizada correctamente.', 'success')
    return redirect(url_for('doctor.dashboard'))
