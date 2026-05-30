from app.utils.db import get_db


class Mascota:

    @staticmethod
    def get_by_id(mascota_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM mascotas WHERE id = %s', (mascota_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def get_by_usuario(usuario_id):
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM mascotas WHERE id_usuario = %s ORDER BY nombre_mascota',
            (usuario_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def create(nombre_mascota, tipo_mascota, edad, id_usuario, descripcion=None):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO mascotas (nombre_mascota, tipo_mascota, edad, descripcion, id_usuario) '
            'VALUES (%s, %s, %s, %s, %s)',
            (nombre_mascota, tipo_mascota, edad, descripcion, id_usuario)
        )
        conn.commit()
        mascota_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return mascota_id

    @staticmethod
    def delete(mascota_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM mascotas WHERE id = %s', (mascota_id,))
        conn.commit()
        cursor.close()
        conn.close()
