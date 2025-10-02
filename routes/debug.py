# routes/debug.py
from flask import Blueprint, jsonify
import os

bp = Blueprint("debug", __name__)

@bp.route("/check-env", methods=["GET"])
def check_env():
    return jsonify({
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_DEST": os.getenv("EMAIL_DEST"),
        "EMAIL_PASS_len": len(os.getenv("EMAIL_PASS") or "")
    })
