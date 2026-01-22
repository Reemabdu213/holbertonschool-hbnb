from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api.v1 import users
from app.api.v1.auth import api as auth
from app.api.v1.protected import api as protected

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # flask-jwt-extended يستخدم SECRET_KEY
    # لازم تكون موجودة في config
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    api.add_namespace(users.api, path='/api/v1/users')
    api.add_namespace(auth, path='/api/v1/auth')
    api.add_namespace(protected, path='/api/v1')

    return app
