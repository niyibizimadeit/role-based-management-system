from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .post_routes import post_bp
from .admin_post_routes import admin_post_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(post_bp, url_prefix="/api")
    app.register_blueprint(admin_post_bp)