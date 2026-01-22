from flask import Flask
from app.extensions import bcrypt, jwt
from app.api.v1 import api_v1_bp

def create_app(config_class="config.DevelopmentConfig"):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration from config class
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(api_v1_bp)
    
    return app
