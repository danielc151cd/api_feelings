from flask import Blueprint, request, jsonify
from config.config import db

bp = Blueprint("sentimientos", __name__)

@bp.route("/crear", methods=["POST", "OPTIONS"])
def crear():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(force=True)
    usuario_id = data.get("usuario_id")
    emocion = data.get("emocion")
    descripcion = data.get("descripcion")

    cur = db.cursor()
    cur.execute(
        "INSERT INTO sentimientos (usuario_id, emocion, descripcion) VALUES (%s, %s, %s)",
        (usuario_id, emocion, descripcion)
    )
    db.commit()
    return jsonify({"msg": "✅ Sentimiento registrado"}), 201

@bp.route("/listar/<int:usuario_id>", methods=["GET"])
def listar(usuario_id):
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM sentimientos WHERE usuario_id=%s ORDER BY fecha DESC",
        (usuario_id,)
    )
    return jsonify(cur.fetchall()), 200
