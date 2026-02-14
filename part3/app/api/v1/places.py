from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # تاسك 4: إضافة get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # تاسك 3: يتطلب تسجيل دخول لإنشاء مكان
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()  # تاسك 3: جلب معرف المستخدم من JWT
        place_data = api.payload
        
        place_data['owner_id'] = current_user  # تاسك 3: تعيين المالك تلقائياً لمنع الانتحال
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):  # تاسك 3: endpoint عام - لا يحتاج تسجيل دخول
        """Get all places (public endpoint)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):  # تاسك 3: endpoint عام - لا يحتاج تسجيل دخول
        """Get place details (public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if hasattr(place, 'to_dict_list'):
            return place.to_dict_list(), 200
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # تاسك 3: يتطلب تسجيل دخول لتعديل المكان
    def put(self, place_id):
        """Update a place"""
        current_user_id = get_jwt_identity()  # تاسك 3: جلب المستخدم الحالي
        current_user = get_jwt()  # تاسك 4: جلب كامل معلومات JWT
        is_admin = current_user.get('is_admin', False)  # تاسك 4: التحقق من Admin
        
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # تاسك 4: التحقق من owner_id بطريقة آمنة
        # التحقق إذا كان owner هو object أو string
        if hasattr(place, 'owner_id'):
            owner_id = place.owner_id
        elif hasattr(place.owner, 'id'):
            owner_id = place.owner.id
        else:
            owner_id = str(place.owner)
        
        # تاسك 4: Admin يتجاوز التحقق من الملكية، User عادي لازم يكون المالك
        if not is_admin and owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403  # تاسك 3: خطأ 403 إذا ما كان المالك
        
        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        for amenity in amenities_data:
            a = facade.get_amenity(amenity['id'])
            if not a:
                return {'error': 'Invalid input data'}, 400
        
        for amenity in amenities_data:
            place.add_amenity(amenity)
        return {'message': 'Amenities added successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
