from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'vetcuidado_secret_key_abp_2026'

# ── Flask-Login ────────────────────────────────────────────────────────────────
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder a esta sección.'

# ── MySQL conexión ─────────────────────────────────────────────────────────────
DB_CONFIG = {
    'host':     '172.17.30.35',
    'port':     3306,
    'database': 'vetcuidado_db',
    'user':     'compañero',
    'password': 'contraseña123',
    'charset':  'utf8mb4'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            nombre   VARCHAR(150) NOT NULL,
            email    VARCHAR(150) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id     INT NOT NULL,
            nombre_dueno   VARCHAR(150) NOT NULL,
            nombre_mascota VARCHAR(100) NOT NULL,
            tipo_mascota   VARCHAR(50)  NOT NULL,
            fecha_cita     VARCHAR(50)  NOT NULL,
            motivo         TEXT         NOT NULL,
            created        DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# ── User model ─────────────────────────────────────────────────────────────────
class User(UserMixin):
    def __init__(self, id, nombre, email):
        self.id     = id
        self.nombre = nombre
        self.email  = email

@login_manager.user_loader
def load_user(user_id):
    conn   = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return User(row['id'], row['nombre'], row['email'])
    return None

# ── Rutas ──────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email  = request.form.get('email', '').strip().lower()
        pwd    = request.form.get('password', '')
        pwd2   = request.form.get('password2', '')

        error = None
        if not nombre or not email or not pwd:
            error = 'Todos los campos son obligatorios.'
        elif pwd != pwd2:
            error = 'Las contraseñas no coinciden.'
        elif len(pwd) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'

        if error:
            flash(error, 'error')
            return render_template('register.html')

        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id FROM usuarios WHERE email = %s', (email,))
        exists = cursor.fetchone()

        if exists:
            cursor.close()
            conn.close()
            flash('Ya existe una cuenta con ese correo electrónico.', 'error')
            return render_template('register.html')

        hashed = generate_password_hash(pwd)
        cursor.execute('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)',
                       (nombre, email, hashed))
        conn.commit()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        login_user(User(row['id'], row['nombre'], row['email']))
        flash(f'¡Bienvenido/a, {nombre}! Tu cuenta ha sido creada.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email  = request.form.get('email', '').strip().lower()
        pwd    = request.form.get('password', '')
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and check_password_hash(row['password'], pwd):
            login_user(User(row['id'], row['nombre'], row['email']))
            flash(f'¡Hola de nuevo, {row["nombre"]}! 🐾', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Correo o contraseña incorrectos.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('home'))

@app.route('/citas')
@login_required
def citas():
    return render_template('citas.html')

@app.route('/api/citas', methods=['POST'])
@login_required
def crear_cita():
    datos  = request.get_json()
    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO citas (usuario_id, nombre_dueno, nombre_mascota, tipo_mascota, fecha_cita, motivo)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (current_user.id, datos.get('nombre_dueno'), datos.get('nombre_mascota'),
          datos.get('tipo_mascota'), datos.get('fecha_cita'), datos.get('motivo')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'mensaje': '¡Cita registrada correctamente!'}), 201

@app.route('/mascotas')
def mascotas():
    return render_template('mascotas.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)