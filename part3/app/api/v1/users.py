#!/usr/bin/env python3
"""
User API endpoints
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # تاسك 4: إضافة get_jwt
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

# تاسك 3: نموذج للتعديل بدون email و password
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# تاسك 4: نموذج Admin للتعديل الكامل (مع email و password)
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'password': fields.String(description='Password')
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
    #@api.response(400, 'Invalid input')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()  # تاسك 4: يتطلب تسجيل دخول
    def post(self):
        """Register a new user (Admin only)"""
        current_user = get_jwt()  # تاسك 4: جلب معلومات المستخدم
        
        if not current_user.get('is_admin'):  # تاسك 4: التحقق من صلاحيات Admin
            return {'error': 'Admin privileges required'}, 403  # تاسك 4: فقط Admin ينشئ مستخدمين
        
        user_data = api.payload
        # Check if email is already in use
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
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
    
    #@api.expect(user_update_model, admin_user_update_model)
    @api.expect(admin_user_update_model) # نستخدم موديل الأدمن لأنه الأشمل للتوثيق
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input')
    @jwt_required()  # تاسك 3 & 4: يتطلب تسجيل دخول
    def put(self, user_id):
        """Update user information"""
        current_user_id = get_jwt_identity()  # تاسك 3: جلب ID المستخدم الحالي
        current_user = get_jwt()  # تاسك 4: جلب كامل معلومات JWT
        is_admin = current_user.get('is_admin', False)  # تاسك 4: التحقق من Admin
        

        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # تاسك 4: Admin يقدر يعدل أي مستخدم، User عادي يعدل نفسه فقط
        if not is_admin and user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403  # تاسك 3: خطأ 403 إذا حاول تعديل غيره
            
        user_data = api.payload
        
        # تاسك 4: Admin يقدر يعدل email و password
        if not is_admin:
            # تاسك 3: User عادي ممنوع من تعديل email و password
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        else:
            # تاسك 4: Admin يقدر يعدل email - نتحقق من التكرار
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400
        
        try:
            # تاسك 4: Admin يقدر يعدل password أيضاً
            if is_admin and 'password' in user_data:
                user.hash_password(user_data['password'])
        
            facade.update_user(user_id, user_data)
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
