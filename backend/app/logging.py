from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt
from datetime import datetime

def log_operation():
    try:
        user_id = get_jwt_identity()
        role = get_jwt().get("role")
    except Exception:
        user_id = None
        role = None

    print({
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.path,
        "user_id": user_id,
        "role": role
    })
