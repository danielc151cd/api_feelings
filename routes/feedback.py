from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # 👈 para leer variables de entorno

bp = Blueprint("feedback", __name__)

# 🔹 Configuración de correo desde variables de entorno
EMAIL_USER = os.getenv("EMAIL_USER")   # tu correo Gmail
EMAIL_PASS = os.getenv("EMAIL_PASS")   # contraseña de aplicación de Gmail
EMAIL_DEST = os.getenv("EMAIL_DEST")   # destino del feedback

@bp.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json(force=True)  # 👈 fuerza a leer JSON
        nombre = data.get("nombre", "Anónimo")
        email = data.get("email", "No proporcionado")
        mensaje = data.get("mensaje", "")

        # Crear mensaje con soporte UTF-8
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_DEST
        msg["Subject"] = f"📩 Nuevo Feedback de {nombre}"

        cuerpo = f"""
        Has recibido un nuevo comentario desde la app:

        👤 Nombre: {nombre}
        📧 Email: {email}

        💬 Mensaje:
        {mensaje}
        """

        msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

        # Enviar por SMTP (Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_DEST, msg.as_string())
        server.quit()

        return jsonify({"msg": "✅ Opinión enviada correctamente"}), 200

    except Exception as e:
        print("❌ Error enviando correo:", e)
        return jsonify({"msg": f"⚠️ Error enviando la opinión: {str(e)}"}), 500
