"""
Flask application initialization
"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig): 
    """Create and configure the Flask application"""
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # ✅ إنشاء الجداول تلقائياً عند بدء التطبيق
    with app.app_context():
        db.create_all()
    
    # Register the API Blueprint
    from app.api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp)
    
    return app
