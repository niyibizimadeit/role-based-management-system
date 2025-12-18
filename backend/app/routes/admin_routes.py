from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.permissions import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/dashboard")
@jwt_required()
@admin_required
def dashboard():
    return jsonify(msg="Admin dashboard")
