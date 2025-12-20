from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post
from app.extensions import db
from app.utils.logger import log_action

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
@post_bp.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    post = Post.query.get_or_404(post_id)

    if post.author_id != user_id:
        return jsonify(error="Forbidden"), 403

    
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    # Reset status so admin re-approves
    post.status = "pending"

    db.session.commit()

    log_action(
        action="Updated post",
        target=f"post_id={post.id}"
    )

    return jsonify(message="Post updated")

@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)

    if post.author_id != user_id:
        return jsonify(error="Forbidden"), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify(message="Post deleted")
