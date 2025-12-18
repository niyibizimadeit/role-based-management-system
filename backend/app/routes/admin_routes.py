from flask import Blueprint
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return {"message": "Welcome Admin"}
