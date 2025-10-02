from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint("feedback", __name__)

# 🔹 Configuración de correo (ajusta con tus datos reales)
EMAIL_USER = "danisancarta@gmail.com"
EMAIL_PASS = "djeh elxz cupc jlrf"  # 👈 contraseña de aplicación de Gmail
EMAIL_DEST = "salasxd1.1.1.2@gmail.com"

@bp.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json()
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

        # 👇 Aquí se fuerza UTF-8
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
