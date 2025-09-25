from flask import Blueprint, request, jsonify
from config.config import db  # Importamos db desde config, NO desde app

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        db.commit()
        return jsonify({"msg": "Usuario registrado correctamente ✅"}), 201
    except Exception as e:
        return jsonify({"msg": "Error en registro", "error": str(e)}), 500
    password = data.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios WHERE email=%s AND password=%s", 
        (email, password)
    )
    user = cursor.fetchone()

    if user:
        return jsonify({"msg": "Login exitoso", "usuario": user})
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401
