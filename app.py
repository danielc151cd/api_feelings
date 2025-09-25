from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"msg": "API Mapa de Sentimientos con MySQL 🗺️"}

# 🔹 Registrar rutas
from routes import auth, sentimientos
app.register_blueprint(auth.bp, url_prefix="/api")
app.register_blueprint(sentimientos.bp, url_prefix="/api/sentimientos")

if __name__ == "__main__":
    app.run(debug=True)
