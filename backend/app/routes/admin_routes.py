from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/ping")
def ping():
    return {"message": "Admin routes working"}
