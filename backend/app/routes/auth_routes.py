from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from app.utils.logger import log_action


from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="Username and password required"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already exists"), 400

    user = User(username=username, role="user")
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201


#Login endpoint

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    print("LOGIN PAYLOAD:", data)   #new line

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(error="Username and password required"), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify(error="Invalid credentials"), 401

    access_token = create_access_token(
    identity=str(user.id),   # MUST be string
    additional_claims={"role": user.role}
    )

    log_action(
        action="Login",
        target=f"user_id={user.id}"
    )


    return jsonify(
        access_token=access_token,
        role=user.role
    ), 200
