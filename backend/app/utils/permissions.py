from functools import wraps
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask import jsonify
from app.models import User, Post

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "ADMIN":
            return jsonify(msg="Admin access required"), 403
        return fn(*args, **kwargs)
    return wrapper


def owner_or_admin_required(model):
    def decorator(fn):
        @wraps(fn)
        def wrapper(id, *args, **kwargs):
            user_id = get_jwt_identity()
            claims = get_jwt()

            obj = model.query.get_or_404(id)

            if claims.get("role") != "ADMIN" and obj.author_id != user_id:
                return jsonify(msg="Not allowed"), 403

            return fn(id, *args, **kwargs)
        return wrapper
    return decorator
