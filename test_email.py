import smtplib
from email.mime.text import MIMEText

EMAIL_USER = "tu_correo@gmail.com"
EMAIL_PASS = "tu_contraseña_app"
EMAIL_DEST = "destinatario@demo.com"

try:
    # Forzar UTF-8
    msg = MIMEText("🚀 Test desde Python (sin Flask con ñ)", "plain", "utf-8")
    msg["Subject"] = "Prueba SMTP desde Flask 🚀"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DEST

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, EMAIL_DEST, msg.as_string())
    server.quit()

    print("✅ Correo enviado correctamente")
except Exception as e:
    print("❌ Error:", e)
