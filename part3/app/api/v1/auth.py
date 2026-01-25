from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """User login"""
        credentials = api.payload
        print(f"=== DEBUG: Login attempt ===")
        print(f"Email received: {credentials['email']}")
        
        user = facade.get_user_by_email(credentials['email'])
        print(f"User found: {user}")
        
        if user:
            print(f"User email in DB: {user.email}")
            print(f"Stored password hash: {user.password[:50]}...")
            verification = user.verify_password(credentials['password'])
            print(f"Password verification result: {verification}")
        else:
            print("No user found with this email!")
        
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        
        return {'access_token': access_token}, 200
