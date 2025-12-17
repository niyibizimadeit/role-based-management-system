from flask import Blueprint

post_bp = Blueprint("posts", __name__)

@post_bp.route("/ping")
def ping():
    return {"message": "Post routes working"}
