from app.utils.db import get_db


class Usuario:

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_by_dni(dni):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE dni = %s', (dni,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def create(nombre_completo, dni, email, password_hash, telefono=None, rol='cliente'):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (nombre_completo, dni, email, password_hash, telefono, rol) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (nombre_completo, dni, email, password_hash, telefono, rol)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return user_id

    @staticmethod
    def get_all(search=None):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        if search:
            cursor.execute(
                'SELECT * FROM usuarios WHERE nombre_completo LIKE %s OR dni LIKE %s ORDER BY created_at DESC',
                (f'%{search}%', f'%{search}%')
            )
        else:
            cursor.execute('SELECT * FROM usuarios ORDER BY created_at DESC')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def delete(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
