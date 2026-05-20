from flask import Flask, render_template, request, jsonify
# Initialize the Flask application
app = Flask(__name__)


# Route for the Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Route for the Appointments Page
@app.route("/citas")
def citas():
    return render_template("citas.html")



@app.route("/api/citas", methods=["POST"])
def crear_cita():
    datos_recibidos = request.get_json()
    print("Datos que llegaron de la web:", datos_recibidos)
    return jsonify({
        "status": "success",
        "mensaje": "¡Cita registrada de forma rápida y segura en el servidor!"
    }), 201


# Route for the Pets Page
@app.route("/mascotas")
def mascotas():
    return render_template("mascotas.html")


# Run the application
if __name__ == "__main__":
    # debug=True allows the server to automatically reload when you make changes
    app.run(debug=True)
