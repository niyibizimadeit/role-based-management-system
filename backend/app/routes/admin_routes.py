from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.utils.permissions import admin_required
from app.models import Post

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/dashboard")
@jwt_required()
@admin_required
def dashboard():
    return jsonify(msg="Admin dashboard")

@admin_bp.route("/posts", methods=["GET"])
@jwt_required()
@admin_required
def get_all_posts():
    posts = Post.query.all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "status": p.status,
            "user_id": p.user_id
        }
        for p in posts
    ])

