from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import AppUser
from app.services.auth_service import AuthService
from app.utils.decorators import client_required


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.tipo == 'cliente':
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        nombre = request.form.get('nombre_completo', '').strip()
        dni = request.form.get('dni', '').strip().upper()
        email = request.form.get('email', '').strip().lower()
        pwd = request.form.get('password', '')
        pwd2 = request.form.get('password2', '')
        telefono = request.form.get('telefono', '').strip() or None

        error = None
        if not nombre or not dni or not email or not pwd:
            error = 'Todos los campos son obligatorios.'
        elif pwd != pwd2:
            error = 'Las contraseñas no coinciden.'
        elif len(pwd) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'

        if error:
            flash(error, 'error')
            return render_template('auth/register.html')

        user_row, error = AuthService.register_cliente(nombre, dni, email, pwd, telefono)
        if error:
            flash(error, 'error')
            return render_template('auth/register.html')

        user = AppUser(
            f'cliente_{user_row.id}',
            user_row.nombre_completo, user_row.email, 'cliente',
            cliente_id=user_row.id, rol=user_row.rol,
            dni=user_row.dni, telefono=user_row.telefono
        )
        login_user(user)
        flash(f'¡Bienvenido/a, {nombre}! Tu cuenta ha sido creada.', 'success')
        return redirect(url_for('main.home'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.tipo == 'cliente':
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        pwd = request.form.get('password', '')

        user_row, error = AuthService.authenticate_cliente(email, pwd)
        if error:
            flash(error, 'error')
            return render_template('auth/login.html')

        user = AppUser(
            f'cliente_{user_row.id}',
            user_row.nombre_completo, user_row.email, 'cliente',
            cliente_id=user_row.id, rol=user_row.rol,
            dni=user_row.dni, telefono=user_row.telefono
        )
        login_user(user)
        flash(f'¡Hola de nuevo, {user_row.nombre_completo}! 🐾', 'success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.home'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('main.home'))
