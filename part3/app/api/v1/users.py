#!/usr/bin/env python3
"""
User API endpoints
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('users', description='User operations')

# User model for input validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

# User update model (without email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200
    
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        try:
            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.expect(user_update_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input')
    @jwt_required()
    def put(self, user_id):
        """Update user information (requires authentication)"""
        current_user = get_jwt_identity()
        
        # Check if user is trying to modify their own data
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        user_data = api.payload
        
        # Check if trying to modify email or password
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400
        
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            facade.update_user(user_id, user_data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
