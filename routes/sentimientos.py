from flask import Blueprint, request, jsonify
from config.config import db

bp = Blueprint("sentimientos", __name__)

@bp.route("/crear", methods=["POST"])
def crear_sentimiento():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    emocion = data.get("emocion")
    descripcion = data.get("descripcion")

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO sentimientos (usuario_id, emocion, descripcion) VALUES (%s, %s, %s)",
        (usuario_id, emocion, descripcion)
    )
    db.commit()
    return jsonify({"msg": "Sentimiento registrado ✅"}), 201

@bp.route("/listar/<int:usuario_id>", methods=["GET"])
def listar_sentimientos(usuario_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sentimientos WHERE usuario_id=%s ORDER BY fecha DESC", (usuario_id,))
    return jsonify(cursor.fetchall())
