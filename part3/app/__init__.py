"""
Flask application initialization
"""
from flask import Flask
from flask_restx import Api
from app.api.v1 import users, places, reviews, amenities
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_class="development"):
    """Create and configure the Flask application"""
    app = Flask(__name__)
     jwt.init_app(app)

    # Load configuration
    from config import config
    app.config.from_object(config[config_class])
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )
    
    # Register namespaces (we'll add these later)
    api.add_namespace(users.api, path='/api/v1/users')
    # api.add_namespace(places.api, path='/api/v1/places')
    # api.add_namespace(reviews.api, path='/api/v1/reviews')
    # api.add_namespace(amenities.api, path='/api/v1/amenities')
    
    return app
