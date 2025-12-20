from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.permissions import admin_required
from app.models import User, Post
from app.models.log import Log
from app.extensions import db
from app.utils.logger import log_action


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
            "author_id": p.author_id
        }
        for p in posts
    ])

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "is_active": u.is_active
        }
        for u in users
    ])


@admin_bp.route("/users", methods=["POST"])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "USER")

    if not username or not password:
        return jsonify(error="Username and password required"), 400

    if role not in ["ADMIN", "USER"]:
        return jsonify(error="Invalid role"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already exists"), 400

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    log_action(
        action="Created user",
        target=f"user_id={user.id}"
    )


    return jsonify(message="User created"), 201


@admin_bp.route("/users/<int:user_id>/role", methods=["PUT"])
@jwt_required()
@admin_required
def update_user_role(user_id):
    admin_id = int(get_jwt_identity())
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in ["ADMIN", "USER"]:
        return jsonify(error="Invalid role"), 400

    if user_id == admin_id:
        return jsonify(error="Cannot change your own role"), 403

    user = User.query.get_or_404(user_id)

    old_role = user.role
    user.role = new_role
    db.session.commit()

    log_action(
        action="CHANGE_ROLE",
        target=f"user_id={user.id}, {old_role} → {new_role}"
    )

    return jsonify(message="Role updated")



@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    admin_id = int(get_jwt_identity())

    if user_id == admin_id:
        return jsonify(error="Cannot delete yourself"), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User deleted")



@admin_bp.route("/posts/<int:id>/approve", methods=["PUT"])
@jwt_required()
@admin_required
def approve_post(id):
    post = Post.query.get_or_404(id)
    post.status = "approved"
    db.session.commit()

    log_action(
        action=f"Post {post.status}",
        target=f"post_id={post.id}"
    )

    return jsonify({"message": "Post approved"})


@admin_bp.route("/posts/<int:id>/reject", methods=["PUT"])
@jwt_required()
@admin_required
def reject_post(id):
    post = Post.query.get_or_404(id)
    post.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Post rejected"})

@admin_bp.route("/logs", methods=["GET"])
@jwt_required()
@admin_required
def get_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).limit(100).all()

    return jsonify([
        {
            "id": l.id,
            "action": l.action,
            "actor_id": l.actor_id,
            "target": l.target,
            "timestamp": l.timestamp.isoformat()
        }
        for l in logs
    ])
