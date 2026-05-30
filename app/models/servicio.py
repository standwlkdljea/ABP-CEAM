from app.utils.db import get_db


class Servicio:

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM servicios')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(servicio_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM servicios WHERE id = %s', (servicio_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
