from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/citas", methods=["GET", "POST"])
def citas():
    if request.method == "POST":
        nombre_dueno   = request.form["nombre_dueno"]
        nombre_mascota = request.form["nombre_mascota"]
        tipo_mascota   = request.form["tipo_mascota"]
        fecha_cita     = request.form["fecha_cita"]
        motivo         = request.form["motivo"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO citas (nombre_dueno, nombre_mascota, tipo_mascota, fecha_cita, motivo)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre_dueno, nombre_mascota, tipo_mascota, fecha_cita, motivo))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('citas'))

    return render_template("citas.html")

@app.route("/mascotas")          # ← esta ruta faltaba
def mascotas():
    return render_template("mascotas.html")

if __name__ == "__main__":
    app.run(debug=True)