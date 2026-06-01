from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.mascota import Mascota
from app.utils.decorators import client_required


mascota_bp = Blueprint('mascotas', __name__)


@mascota_bp.route('/mascotas')
@login_required
@client_required
def listar():
    mascotas = Mascota.get_by_usuario(current_user.cliente_id)
    return render_template('mascotas/list.html', mascotas=mascotas)


@mascota_bp.route('/mascotas/crear', methods=['GET', 'POST'])
@login_required
@client_required
def crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre_mascota', '').strip()
        tipo = request.form.get('tipo_mascota', '').strip()
        edad = request.form.get('edad', '').strip()
        descripcion = request.form.get('descripcion', '').strip() or None

        error = None
        if not nombre or not tipo or not edad:
            error = 'Todos los campos obligatorios deben completarse.'
        elif not edad.isdigit() or int(edad) < 0:
            error = 'La edad debe ser un número válido.'

        if error:
            flash(error, 'error')
            return render_template('mascotas/create.html')

        Mascota.create(nombre, tipo, int(edad), current_user.cliente_id, descripcion)
        flash(f'¡{nombre} ha sido registrado/a!', 'success')
        return redirect(url_for('mascotas.listar'))

    return render_template('mascotas/create.html')


@mascota_bp.route('/mascotas/<int:mascota_id>/eliminar', methods=['POST'])
@login_required
@client_required
def eliminar(mascota_id):
    mascota = Mascota.get_by_id(mascota_id)
    if not mascota or mascota.id_usuario != current_user.cliente_id:
        flash('Mascota no encontrada.', 'error')
        return redirect(url_for('mascotas.listar'))

    Mascota.delete(mascota_id)
    flash('Mascota eliminada correctamente.', 'success')
    return redirect(url_for('mascotas.listar'))
