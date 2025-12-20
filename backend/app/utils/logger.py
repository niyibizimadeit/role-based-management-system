from app.extensions import db
from app.models import Log
from flask_jwt_extended import get_jwt_identity

def log_action(action, target=None):
    try:
        actor_id = get_jwt_identity()
    except:
        actor_id = None

    entry = Log(
        action=action,
        actor_id=actor_id,
        target=target
    )

    db.session.add(entry)
    db.session.commit()
