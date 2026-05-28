from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
# Necesario para poder usar sesiones seguras en Flask
app.secret_key = 'tu_clave_secreta_super_segura_para_el_proyecto' 

# =========================================================================
# DECORADOR DE SEGURIDAD (Control de Roles)
# =========================================================================
def requiere_rol(rol_permitido):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            # 1. Comprobamos si hay un usuario logueado en la sesión
            if 'rol' not in session:
                return redirect(url_for('login_page'))
            
            # 2. Comprobamos si su rol coincide con el permitido
            if session['rol'] != rol_permitido:
                # Si un 'usuario' intenta entrar a una ruta de 'doctor', le denegamos el acceso
                return render_template("403.html"), 403 
            
            return f(*args, **kwargs)
        return funcion_decorada
    return decorador

# =========================================================================
# RUTAS DE AUTENTICACIÓN (Simulación de consulta a Base de Datos)
# =========================================================================

@app.route("/login")
def login_page():
    return render_template("login.html") # Crea este HTML con tu formulario

@app.route("/api/login", methods=["POST"])
def procesar_login():
    datos = request.get_json()
    email = datos.get("email")
    password = datos.get("password")
    tipo_login = datos.get("tipo") # Puede ser 'usuario' o 'doctor'

    # NOTA: Aquí deberías hacer una Query a tu MySQL real. 
    # Ejemplo: SELECT * FROM usuarios WHERE email = %s
    
    # --- SIMULACIÓN DE LOGIN EXITOSO ---
    if tipo_login == "usuario" and email == "carlos@gmail.com" and password == "1234":
        session['user_id'] = 1
        session['nombre'] = "Carlos García"
        session['rol'] = "usuario" # <--- Guardamos el Rol
        return jsonify({"status": "success", "redirigir": url_for("citas")}), 200

    elif tipo_login == "doctor" and email == "mendoza@vetcuidado.com" and password == "doctor123":
        session['user_id'] = 1
        session['nombre'] = "Dr. Carlos Mendoza"
        session['rol'] = "doctor" # <--- Guardamos el Rol
        return jsonify({"status": "success", "redirigir": url_for("panel_doctor")}), 200
    
    # Si las credenciales fallan
    return jsonify({"status": "error", "mensaje": "Credenciales incorrectas"}), 401

@app.route("/logout")
def logout():
    session.clear() # Limpia la sesión por completo al salir
    return redirect(url_for('auth.home'))

# =========================================================================
# VISTAS PÚBLICAS Y PROTEGIDAS
# =========================================================================

@app.route("/")
def home():
    return render_template("index.html")

# Vista protegida: Solo pueden entrar los CLIENTES (usuarios)
@app.route("/citas")
@requiere_rol('usuario')
def citas():
    return render_template("citas.html")

# Vista protegida: Solo pueden entrar los DOCTORES
@app.route("/panel-doctor")
@requiere_rol('doctor')
def panel_doctor():
    # Aquí puedes retornar tu vista de gestión de mascotas o el historial de citas médicas
    return render_template("mascotas.html") 

@app.route("/api/citas", methods=["POST"])
@requiere_rol('usuario') # Solo usuarios logueados pueden enviar citas
def crear_cita():
    datos_recibidos = request.get_json()
    print(f"Cita creada por el usuario {session['nombre']}:", datos_recibidos)
    return jsonify({"status": "success", "mensaje": "¡Cita registrada!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
