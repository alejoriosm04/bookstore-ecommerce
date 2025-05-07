from flask import Flask
from .routes import configure_routes
from .middleware.auth_middleware import jwt_manager
from .middleware.error_handler import handle_errors

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.Config')
    
    # Initialize extensions
    jwt_manager.init_app(app)
    
    # Register error handlers
    handle_errors(app)
    
    # Configure routes
    configure_routes(app)
    
    return app