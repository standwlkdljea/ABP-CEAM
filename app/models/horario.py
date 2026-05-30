from app.utils.db import get_db


class HorarioTrabajo:

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM horarios_trabajo ORDER BY dia_semana')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_dia(dia_semana):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM horarios_trabajo WHERE dia_semana = %s', (dia_semana,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
