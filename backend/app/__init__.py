from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate, cors
from .errors import register_error_handlers
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register error handlers
    register_routes(app)
    register_error_handlers(app)

    return app

