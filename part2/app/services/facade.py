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

    # =====================
    # User methods (Part 2)
    # =====================
    def create_user(self, user_data):
        email = user_data['email'].strip().lower()
        if self.user_repo.get_by_attribute('email', email):
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=email,
            is_admin=user_data.get('is_admin', False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        if not email:
            return None
        return self.user_repo.get_by_attribute('email', email.strip().lower())

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if 'email' in data and data['email'] is not None:
            new_email = data['email'].strip().lower()
            existing = self.user_repo.get_by_attribute('email', new_email)
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
            data['email'] = new_email

        return self.user_repo.update(user_id, data)

    def get_all_users(self):
        """Retrieve all users"""
        return self.user_repo.get_all()

    # =====================
    # Amenity methods
    # =====================
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # =====================
    # Place methods
    # =====================
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

        return self.place_repo.update(place_id, data)

    # =====================
    # Review methods
    # =====================
    def create_review(self, review_data):
        if not isinstance(review_data, dict):
            raise ValueError("Invalid input data")

        text = (review_data.get("text") or "").strip()
        rating = review_data.get("rating")
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")

        if not text:
            raise ValueError("text is required")
        if rating is None or not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        if not user_id:
            raise ValueError("user_id is required")
        if not place_id:
            raise ValueError("place_id is required")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=text,
            rating=rating,
            place=place,
            user=user
        )

        self.review_repo.add(review)

        if hasattr(place, "add_review"):
            place.add_review(review)
        elif hasattr(place, "reviews"):
            place.reviews.append(review)

        if hasattr(user, "add_review"):
            user.add_review(review)
        elif hasattr(user, "reviews"):
            user.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if hasattr(place, "reviews"):
            return place.reviews
        return []

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if not isinstance(review_data, dict):
            raise ValueError("Invalid input data")

        if "text" in review_data:
            new_text = (review_data.get("text") or "").strip()
            if not new_text:
                raise ValueError("text cannot be empty")
            review_data["text"] = new_text

        if "rating" in review_data:
            new_rating = review_data.get("rating")
            if new_rating is None or not isinstance(new_rating, int) or not (1 <= new_rating <= 5):
                raise ValueError("rating must be an integer between 1 and 5")

        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = getattr(review, "place", None)
        user = getattr(review, "user", None)

        if place and hasattr(place, "reviews"):
            place.reviews = [r for r in place.reviews if getattr(r, "id", None) != review_id]

        if user and hasattr(user, "reviews"):
            user.reviews = [r for r in user.reviews if getattr(r, "id", None) != review_id]

        self.review_repo.delete(review_id)
        return True
