from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        # Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # DEBUG: Check if user exists
        print(f"DEBUG: User found: {user is not None}")
        if user:
            print(f"DEBUG: User ID: {user.id}")
            print(f"DEBUG: User has password attr: {hasattr(user, 'password')}")
            if hasattr(user, 'password'):
                print(f"DEBUG: Password value exists: {user.password is not None}")
                print(f"DEBUG: Password starts with: {user.password[:10] if user.password else 'None'}")
        
        # Check if the user exists and the password is correct
        if not user:
            print("DEBUG: User not found")
            return {'error': 'Invalid credentials'}, 401
        
        # DEBUG: Try password verification
        try:
            password_valid = user.verify_password(credentials['password'])
            print(f"DEBUG: Password verification result: {password_valid}")
        except Exception as e:
            print(f"DEBUG: Password verification error: {type(e).__name__}: {e}")
            return {'error': 'Invalid credentials'}, 401
        
        if not password_valid:
            print("DEBUG: Password verification returned False")
            return {'error': 'Invalid credentials'}, 401
        
        try:
            # Create a JWT token with the user's id and is_admin flag
            access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
        except Exception as e:
            return {'error': str(e).strip("'")}, 500
        
        # Return the JWT token to the client
        return {'access_token': access_token}, 200
