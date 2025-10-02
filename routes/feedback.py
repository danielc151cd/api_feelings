from flask import Blueprint, request, jsonify
import os
import requests

bp = Blueprint("feedback", __name__)

# 🔹 Configuración desde variables de entorno
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_FROM = os.getenv("MAILGUN_FROM", f"postmaster@{MAILGUN_DOMAIN}")  # 👈 CORREGIDO
MAILGUN_DEST = os.getenv("MAILGUN_DEST")

@bp.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json(force=True)
        nombre = data.get("nombre", "Anónimo")
        email = data.get("email", "No proporcionado")
        mensaje = data.get("mensaje", "")

        cuerpo = f"""
        Has recibido un nuevo comentario desde la app:

        👤 Nombre: {nombre}
        📧 Email: {email}

        💬 Mensaje:
        {mensaje}
        """

        # 🔹 Envío con Mailgun API
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": MAILGUN_FROM,
                "to": [MAILGUN_DEST],
                "subject": f"📩 Nuevo Feedback de {nombre}",
                "text": cuerpo
            }
        )

        if response.status_code == 200:
            return jsonify({"msg": "✅ Opinión enviada correctamente"}), 200
        else:
            return jsonify({
                "msg": "⚠️ Error enviando la opinión",
                "details": response.text
            }), 500

    except Exception as e:
        print("❌ Error enviando correo:", e)
        return jsonify({"msg": f"⚠️ Error enviando la opinión: {str(e)}"}), 500
