from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import Post
from app.utils.permissions import admin_required

admin_post_bp = Blueprint(
    "admin_posts",
    __name__,
    url_prefix="/api/admin/posts"
)

@admin_post_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def all_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@admin_post_bp.route("/<int:id>/approve", methods=["PUT"])
@jwt_required()
@admin_required
def approve_post(id):
    post = Post.query.get_or_404(id)
    post.status = "PUBLISHED"
    db.session.commit()
    return jsonify(msg="Post approved")


@admin_post_bp.route("/<int:id>/reject", methods=["PUT"])
@jwt_required()
@admin_required
def reject_post(id):
    post = Post.query.get_or_404(id)
    post.status = "REJECTED"
    db.session.commit()
    return jsonify(msg="Post rejected")


