from flask import Blueprint
from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api = Api(api_v1_bp, title='HBnB API', version='1.0')

api.add_namespace(users_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(protected_ns, path='/protected')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
