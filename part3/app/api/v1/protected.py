from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('protected', description='Protected operations')

@api.route('/')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """Access a protected endpoint"""
        current_user_id = get_jwt_identity()
        return {
            'message': f'Hello, user {current_user_id}'
        }, 200
