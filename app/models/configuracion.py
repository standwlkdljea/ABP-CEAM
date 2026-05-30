from app.utils.db import get_db


class Configuracion:

    @staticmethod
    def get(clave):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT valor FROM configuraciones WHERE clave = %s', (clave,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['valor'] if row else None

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM configuraciones')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {row['clave']: row['valor'] for row in rows}
