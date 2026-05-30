from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.cita_service import CitaService
from app.models.mascota import Mascota
from app.models.servicio import Servicio
from app.services.horario_service import HorarioService
from app.utils.decorators import client_required


cita_bp = Blueprint('citas', __name__, url_prefix='/citas')


@cita_bp.route('')
@login_required
@client_required
def listar():
    citas = CitaService.get_citas_usuario(current_user.cliente_id)
    return render_template('citas/list.html', citas=citas)


@cita_bp.route('/agendar')
@login_required
@client_required
def agendar_form():
    mascotas = Mascota.get_by_usuario(current_user.cliente_id)
    servicios = Servicio.get_all()
    return render_template('citas/book.html', mascotas=mascotas, servicios=servicios)


@cita_bp.route('/api/agendar', methods=['POST'])
@login_required
@client_required
def agendar_api():
    datos = request.get_json()
    id_mascota = datos.get('id_mascota')
    servicio_id = datos.get('servicio_id')
    inicio = datos.get('inicio')
    motivo = datos.get('motivo', '').strip()

    if not id_mascota or not servicio_id or not inicio or not motivo:
        return jsonify({'status': 'error', 'mensaje': 'Todos los campos son obligatorios.'}), 400

    mascota = Mascota.get_by_id(int(id_mascota))
    if not mascota or mascota['id_usuario'] != current_user.cliente_id:
        return jsonify({'status': 'error', 'mensaje': 'Mascota no encontrada.'}), 400

    cita_id, errors = CitaService.agendar_cita(
        int(id_mascota), int(servicio_id), inicio, motivo
    )

    if errors:
        return jsonify({'status': 'error', 'mensaje': errors[0]}), 400

    return jsonify({'status': 'success', 'mensaje': '¡Cita registrada correctamente!'}), 201


@cita_bp.route('/<int:cita_id>/cancelar', methods=['POST'])
@login_required
@client_required
def cancelar(cita_id):
    CitaService.cancelar_cita(cita_id)
    flash('Cita cancelada correctamente.', 'success')
    return redirect(url_for('citas.listar'))


@cita_bp.route('/api/horario')
@login_required
def horario_api():
    fecha_str = request.args.get('fecha')
    if not fecha_str:
        return jsonify({'status': 'error', 'mensaje': 'Fecha requerida.'}), 400

    from datetime import datetime
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'status': 'error', 'mensaje': 'Formato de fecha inválido.'}), 400

    horario = HorarioService.obtener_horario(fecha)
    if not horario:
        return jsonify({'status': 'error', 'mensaje': 'La clínica no abre ese día.', 'laboral': False})

    return jsonify({
        'status': 'success',
        'laboral': True,
        'hora_apertura': str(horario['hora_apertura']),
        'hora_cierre': str(horario['hora_cierre'])
    })
