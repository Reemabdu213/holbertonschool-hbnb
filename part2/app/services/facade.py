#!/usr/bin/env python3
"""
HBnB Facade
"""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade Pattern"""
    
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    def create_user(self, user_data):
        existing_users = self.user_repo.get_all()
        for user in existing_users:
            if user.email == user_data.get('email', '').strip().lower():
                raise ValueError("Email already exists")
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        if 'email' in data:
            new_email = data['email'].strip().lower()
            for existing_user in self.user_repo.get_all():
                if existing_user.email == new_email and existing_user.id != user_id:
                    raise ValueError("Email already exists")
        
        user.update(data)
        self.user_repo.update(user_id, user)
        return user
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        amenity.update(data)
        self.amenity_repo.update(amenity_id, amenity)
        return amenity
    
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
        
        self.place_repo.add(place)
        owner.add_place(place)
        
        return place
    
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()
    
    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        if 'amenities' in data:
            place.amenities = []
            for amenity_id in data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
            del data['amenities']
        
        place.update(data)
        self.place_repo.update(place_id, place)
        return place
    
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
        
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        
        self.review_repo.add(review)
        place.add_review(review)
        user.add_review(review)
        
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place.id == place_id]
    
    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        review.update(data)
        self.review_repo.update(review_id, review)
        return review
    
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        self.review_repo.delete(review_id)
        return True
