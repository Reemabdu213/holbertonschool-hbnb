"""
Flask application initialization
"""
from flask import Flask
from flask_restx import Api
from app.api.v1 import users, places, reviews, amenities
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager #المكتبه الي تتعامل مع JWT TOKENS عشان تفعل النظام 
from app.api.v1.auth import api as auth

bcrypt = Bcrypt()
jwt = JWTManager() # ربط مع FLASK 

def create_app(config_class="development"):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    bcrypt.init_app(app)
    jwt.init_app(app) # ربط JWT مع التطبيق 
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
    api.add_namespace(auth, path='/api/v1/auth') # part3 ربط صفحات تسجيل الدخول بالمسار حقها
    # api.add_namespace(places.api, path='/api/v1/places')
    # api.add_namespace(reviews.api, path='/api/v1/reviews')
    # api.add_namespace(amenities.api, path='/api/v1/amenities')
    
    return app
