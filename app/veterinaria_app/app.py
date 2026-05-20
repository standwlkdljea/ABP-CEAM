from flask import Flask, render_template, request, jsonify
from db import get_connection  # ← added from snippet 2

app = Flask(__name__)


# ---------- Home ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- Citas (GET only – shows the form) ----------
@app.route("/citas")
def citas():
    return render_template("citas.html")


# ---------- API endpoint to create a new cita (POST, JSON) ----------
@app.route("/api/citas", methods=["POST"])
def crear_cita():
    try:
        # Expect JSON data (as in snippet 1)
        datos = request.get_json()
        print("Datos recibidos:", datos)

        # Extract fields (same names as in snippet 2's form)
        nombre_dueno = datos.get("nombre_dueno")
        nombre_mascota = datos.get("nombre_mascota")
        tipo_mascota = datos.get("tipo_mascota")
        fecha_cita = datos.get("fecha_cita")
        motivo = datos.get("motivo")
        dni_dueno = datos.get("dni_dueno")
        email_dueno = datos.get("email_dueno")

        # Validate required fields (basic check)
        if not all([nombre_dueno, nombre_mascota, tipo_mascota, fecha_cita, motivo]):
            return jsonify(
                {"status": "error", "mensaje": "Faltan campos obligatorios"}
            ), 400

        # Insert into database (using db logic from snippet 2)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
    INSERT INTO citas (nombre_dueno, dni_dueno, email_dueno, nombre_mascota, tipo_mascota, fecha_cita, motivo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""",
            (
                nombre_dueno,
                dni_dueno,
                email_dueno,
                nombre_mascota,
                tipo_mascota,
                fecha_cita,
                motivo,
            ),
        )
        conn.commit()

        # Clean up
        cursor.close()
        conn.close()

        return jsonify(
            {
                "status": "success",
                "mensaje": "¡Cita registrada de forma rápida y segura en el servidor!",
            }
        ), 201

    except Exception as e:
        print("Error al insertar en la base de datos:", e)
        return jsonify(
            {"status": "error", "mensaje": "Error interno del servidor"}
        ), 500


# ---------- Pets page ----------
@app.route("/mascotas")
def mascotas():
    return render_template("mascotas.html")


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
