from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post
from app.extensions import db

post_bp = Blueprint("posts", __name__, url_prefix="/api")


@post_bp.route("/posts", methods=["OPTIONS"])
def posts_options():
    return "", 200


@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    identity = get_jwt_identity()
    user_id = identity["id"] if isinstance(identity, dict) else identity

    data = request.get_json()

    post = Post(
        title=data["title"],
        content=data["content"],
        author_id=user_id,
        status="pending"
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created"}), 201


@post_bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():
    identity = get_jwt_identity()
    user_id = identity["id"] if isinstance(identity, dict) else identity

    posts = Post.query.filter_by(author_id=user_id).all()

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "status": p.status,
        }
        for p in posts
    ])
