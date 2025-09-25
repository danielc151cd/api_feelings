import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3310",   # Ajusta al puerto correcto
    password="1234",
    database="mapa_sentimientos"
)

cursor = db.cursor(dictionary=True)
