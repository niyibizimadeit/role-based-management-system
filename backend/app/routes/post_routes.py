from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post
from app.extensions import db
from app.utils.permissions import owner_or_admin_required

post_bp = Blueprint("posts", __name__, url_prefix="/api/posts")

@post_bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()

    post = Post(
    title=data["title"],
    content=data["content"],
    author_id=user_id,
    status="PENDING"
 )

    db.session.add(post)
    db.session.commit()

    return jsonify(msg="Post created"), 201

@post_bp.route("", methods=["GET"])
def get_posts():
    posts = Post.query.filter_by(status="PUBLISHED").all()
    return jsonify([p.to_dict() for p in posts])

@post_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@owner_or_admin_required(Post)
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify(msg="Post deleted")
