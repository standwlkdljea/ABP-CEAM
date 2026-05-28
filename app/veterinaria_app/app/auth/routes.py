from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario, Doctor
from . import auth_blueprint


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login_client():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash("Por favor ingresa correo y contraseña.")
            return render_template("login_client.html")

        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("client.citas"))
        flash("Correo o contraseña incorrectos.")
    return render_template("login_client.html")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register_client():
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            flash("La contraseña es obligatoria.")
            return render_template("register_client.html")

        data = {
            "nombre_completo": request.form.get("full_name"),
            "dni": request.form.get("dni"),
            "email": request.form.get("email"),
            "telefono": request.form.get("phone"),
            "password_hash": generate_password_hash(password),
        }
        if Usuario.query.filter_by(email=data["email"]).first():
            flash("El correo ya está registrado.")
            return render_template("register_client.html")
        
        user = Usuario(**data)  # type: ignore
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("client.mascotas"))
    return render_template("register_client.html")


@auth_blueprint.route("/staff/login", methods=["GET", "POST"])
def login_staff():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash("Por favor ingresa correo y contraseña.")
            return render_template("login_staff.html")

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and check_password_hash(doctor.password_hash, password):
            login_user(doctor)
            return redirect(url_for("staff.dashboard"))
        flash("Credenciales inválidas para el personal.")
    return render_template("login_staff.html")


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@auth_blueprint.route("/")
def home():
    from flask_login import current_user

    return render_template("index.html")