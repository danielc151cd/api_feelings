from flask import Blueprint, request, jsonify
from config.config import db   # Importamos la conexión MySQL
import mysql.connector     # Para capturar errores específicos

# Creamos el blueprint para las rutas de autenticación
bp = Blueprint("auth", __name__)

# ====================================================
# 🔹 Registro de usuarios
# ====================================================
@bp.route("/register", methods=["POST"])
def register():
    """
    Endpoint para registrar un nuevo usuario en la base de datos.
    Espera un JSON con: nombre, email, password
    """
    try:
        # Obtenemos el JSON enviado desde Flutter
        data = request.get_json(force=True)
        print("📥 Datos recibidos en registro:", data)

        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")

        # Validar que no falten campos
        if not nombre or not email or not password:
            return jsonify({"msg": "❌ Faltan campos obligatorios"}), 400

        # Ejecutar la inserción en MySQL
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        db.commit()

        return jsonify({"msg": "✅ Usuario registrado correctamente"}), 201

    except mysql.connector.IntegrityError as e:
        # Error 1062 = clave duplicada (correo ya existe)
        if e.errno == 1062:
            return jsonify({"msg": "❌ El correo ya está en uso"}), 409
        return jsonify({"msg": "Error de integridad", "error": str(e)}), 400

    except Exception as e:
        print("❌ Error en registro:", e)
        return jsonify({"msg": "Error en registro", "error": str(e)}), 500


# ====================================================
# 🔹 Login de usuarios
# ====================================================
@bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint para iniciar sesión.
    Espera un JSON con: email, password
    """
    try:
        # Obtenemos el JSON enviado desde Flutter
        data = request.get_json(force=True)
        print("📥 Datos recibidos en login:", data)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "❌ Faltan credenciales"}), 400

        # Consultar en la BD si el usuario existe
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            # Quitamos la contraseña del JSON por seguridad
            user.pop("password", None)
            return jsonify({"msg": "✅ Login exitoso", "usuario": user}), 200
        else:
            return jsonify({"msg": "❌ Credenciales inválidas"}), 401

    except Exception as e:
        print("❌ Error en login:", e)
        return jsonify({"msg": "Error en login", "error": str(e)}), 500
