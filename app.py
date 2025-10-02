from flask import Flask
from flask_cors import CORS
import os
from routes import auth, sentimientos, feedback # 👈 añade feedback


app = Flask(__name__)

# CORS abierto para /api/*
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True
)

@app.after_request
def add_cors_headers(resp):
    # Refuerza headers para preflight
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return resp

@app.route("/", methods=["GET"])
def home():
    return {"msg": "API Mapa de Sentimientos con MySQL 🗺️"}

# Registrar blueprints DESPUÉS de crear app y CORS
from routes import auth, sentimientos
app.register_blueprint(auth.bp, url_prefix="/api")
app.register_blueprint(sentimientos.bp, url_prefix="/api/sentimientos")
app.register_blueprint(feedback.bp, url_prefix="/api")  # 👈 ahora feedback


# (opcional) imprime rutas para verificar
print("🔎 Rutas registradas:")
for r in app.url_map.iter_rules():
    print(r)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)