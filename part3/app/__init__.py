"""
Flask application initialization
"""
from flask import Flask
from flask_restx import Api
from app.api.v1 import users, places, reviews, amenities
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1.auth import api as auth

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig): 
    """Create and configure the Flask application"""
    
    app = Flask(__name__)   # ✅ تصحيح __name__
    app.config.from_object(config_class)  # ✅ استخدام المتغير

    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )
    
    # Register namespaces
    api.add_namespace(users.api, path='/api/v1/users')
    api.add_namespace(auth, path='/api/v1/auth')

    # api.add_namespace(places.api, path='/api/v1/places')
    # api.add_namespace(reviews.api, path='/api/v1/reviews')
    # api.add_namespace(amenities.api, path='/api/v1/amenities')

    return app   # ✅ مهم جدًا
