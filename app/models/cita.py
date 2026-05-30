from app.utils.db import get_db


class Cita:

    @staticmethod
    def get_by_id(cita_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM citas WHERE id = %s', (cita_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_by_usuario(usuario_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT c.*, m.nombre_mascota, m.tipo_mascota,
                   d.nombre_doctor, s.nombre AS nombre_servicio
            FROM citas c
            JOIN mascotas m ON c.id_mascota = m.id
            JOIN doctores d ON c.id_doctor = d.id
            JOIN servicios s ON c.servicio_id = s.id
            WHERE m.id_usuario = %s
            ORDER BY c.inicio DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_doctor(doctor_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT c.*, m.nombre_mascota, m.tipo_mascota,
                   s.nombre AS nombre_servicio
            FROM citas c
            JOIN mascotas m ON c.id_mascota = m.id
            JOIN servicios s ON c.servicio_id = s.id
            WHERE c.id_doctor = %s
            ORDER BY c.inicio DESC
        ''', (doctor_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_overlapping(doctor_id, inicio, fin):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT * FROM citas
            WHERE id_doctor = %s
              AND estado = 'programada'
              AND inicio < %s
              AND DATE_ADD(inicio, INTERVAL (
                  SELECT duracion_minutos FROM servicios WHERE id = citas.servicio_id
              ) MINUTE) > %s
        ''', (doctor_id, fin, inicio))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def create(inicio, motivo, servicio_id, id_mascota, id_doctor):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO citas (inicio, motivo, servicio_id, id_mascota, id_doctor) '
            'VALUES (%s, %s, %s, %s, %s)',
            (inicio, motivo, servicio_id, id_mascota, id_doctor)
        )
        conn.commit()
        cita_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return cita_id

    @staticmethod
    def update_estado(cita_id, estado):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE citas SET estado = %s WHERE id = %s', (estado, cita_id))
        conn.commit()
        cursor.close()
        conn.close()
