from app.utils.db import get_db


class HistorialCita:

    @staticmethod
    def create(cita_id, doctor_id, estado, observaciones=None):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO historial_citas (cita_id, doctor_id, estado, observaciones) '
            'VALUES (%s, %s, %s, %s)',
            (cita_id, doctor_id, estado, observaciones)
        )
        conn.commit()
        hist_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return hist_id

    @staticmethod
    def get_by_cita(cita_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM historial_citas WHERE cita_id = %s', (cita_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
