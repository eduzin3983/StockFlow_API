"""
Application factory module.

Initializes and configures the Flask application, database, migrations,
and registers all route blueprints.
"""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from app.infraDB.config.connection import db


def create_app():
    """
    Factory function to create and configure the Flask app.

    Returns:
        Flask: A configured Flask application instance.
    """
    # Instantiate the Flask application
    app = Flask(__name__)
    # Load configuration settings from the Config object
    app.config.from_object(Config)

    # Enable CORS for all domains and methods
    CORS(app, 
         origins="*",  # Allow all origins
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allow all common methods
         allow_headers=["Content-Type", "Authorization"],  # Allow common headers
         supports_credentials=True)  # Allow credentials if needed

    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)
    # Initialize Flask-Migrate for database migrations support
    Migrate(app, db)

    # Register authentication routes
    from app.routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)

    # Register product management routes
    from app.routes.product_route import product_bp
    app.register_blueprint(product_bp)

    # Register transaction handling routes
    from app.routes.transaction_route import transaction_bp
    app.register_blueprint(transaction_bp)

    # Register user management routes
    from app.routes.user_route import user_bp
    app.register_blueprint(user_bp)

    # Import models within application context for Alembic autogeneration
    with app.app_context():
        from app.infraDB.models import products, users, transactions

    # Return the configured Flask app
    return app