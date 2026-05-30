from app.utils.db import get_db


class Doctor:

    @staticmethod
    def get_by_id(doctor_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM doctores WHERE id = %s', (doctor_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM doctores WHERE email = %s', (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_all_active():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM doctores WHERE estado = %s', ('activo',))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_servicio(servicio_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM doctores WHERE servicio_id = %s AND estado = %s',
            (servicio_id, 'activo')
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def set_estado(doctor_id, estado):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE doctores SET estado = %s WHERE id = %s', (estado, doctor_id))
        conn.commit()
        cursor.close()
        conn.close()
