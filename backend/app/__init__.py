from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate, cors
from .routes import register_routes
from .errors import register_error_handlers
from .logging import log_operation

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_request
    def before_request_logging():
        log_operation()

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Import models AFTER app & db are ready
    from . import models

    # Register routes & errors
    register_routes(app)
    register_error_handlers(app)

    return app
