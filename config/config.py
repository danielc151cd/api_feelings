import os
import mysql.connector

# 🔹 Conexión a MySQL en Railway
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "switchyard.proxy.rlwy.net"),   # Host Railway
    user=os.getenv("DB_USER", "root"),                       # Usuario
    password=os.getenv("DB_PASSWORD", "iimxEZNJUsobsVCdEdoRHrkHRTeMllSs"),  # Contraseña
    database=os.getenv("DB_NAME", "railway"),                # Nombre de BD (usa 'railway')
    port=int(os.getenv("DB_PORT", 16017))                    # Puerto Railway
)
