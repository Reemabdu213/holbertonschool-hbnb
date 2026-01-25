#!/usr/bin/python3
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)"""
        current_user = get_jwt_identity()
        data = api.payload
        
        # Set user_id to current user
        data['user_id'] = current_user
        
        # Get the place
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if user is trying to review their own place
        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place'}, 400
        
        # Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(data['place_id'])
        for review in existing_reviews:
            if review.user.id == current_user:
                return {'error': 'You have already reviewed this place'}, 400
        
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get all reviews (public endpoint)"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details (public endpoint)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review (requires authentication and ownership)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check ownership - use review.user.id instead of review.user_id
        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        try:
            facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (requires authentication and ownership)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check ownership - use review.user.id instead of review.user_id
        if review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
