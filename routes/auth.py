from flask import Blueprint, request, jsonify
from config.config import db
import mysql.connector

bp = Blueprint("auth", __name__)

# ---------------------
# Helpers CORS (preflight)
# ---------------------
def _ok_options():
    # Responder a preflight OPTIONS con 204
    return ("", 204)

# ---------------------
# Registro
# ---------------------
@bp.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return ("", 204)

    try:
        data = request.get_json(force=True)
        nombre = data.get("nombre")
        email = data.get("email")
        password = data.get("password")

        if not nombre or not email or not password:
            return jsonify({"msg": "❌ Faltan campos obligatorios"}), 400

        cur = db.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )
        db.commit()
        user_id = cur.lastrowid
        cur.close()

        # 🔹 Traer el usuario recién creado y devolverlo
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id, nombre, email FROM usuarios WHERE id=%s", (user_id,))
        nuevo = cur.fetchone()
        cur.close()

        return jsonify({
            "msg": "✅ Usuario registrado correctamente",
            "usuario": nuevo
        }), 201

    except mysql.connector.IntegrityError as e:
        if e.errno == 1062:
            return jsonify({"msg": "❌ El correo ya está en uso"}), 409
        return jsonify({"msg": "Error en registro", "error": str(e)}), 400
    except Exception as e:
        print("❌ Error en /register:", e)
        return jsonify({"msg": "Error en registro", "error": str(e)}), 500

# ---------------------
# Login
# ---------------------
@bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return _ok_options()

    try:
        data = request.get_json(force=True)
        print("📥 /login ->", data)

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "❌ Faltan credenciales"}), 400

        cur = db.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()
        print("🔎 user ->", user)

        if not user:
            return jsonify({"msg": "❌ Credenciales inválidas"}), 401

        user.pop("password", None)
        return jsonify({"msg": "✅ Login exitoso", "usuario": user}), 200

    except Exception as e:
        print("❌ Error en /login:", e)
        return jsonify({"msg": "Error en login", "error": str(e)}), 500
