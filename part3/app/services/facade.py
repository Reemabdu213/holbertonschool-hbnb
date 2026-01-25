from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    # ========== User Methods ==========
    def create_user(self, user_data):
        """Create a new user with hashed password"""
        email = user_data['email'].strip().lower()
        
        if self.user_repo.get_by_attribute('email', email):
            raise ValueError("Email already registered")
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=email,
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        
        self.user_repo.add(user)
        return user
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()
    
    def get_user_by_email(self, email):
        """Get user by email"""
        normalized_email = email.strip().lower()
        return self.user_repo.get_by_attribute('email', normalized_email)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        
        return user
    
    # ========== Place Methods ==========
    def create_place(self, place_data):
        """Create a new place"""
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
        
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        place.update(place_data)
        return place
    
    # ========== Review Methods ==========
    def create_review(self, review_data):
        """Create a new review"""
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        
        self.review_repo.add(review)
        place.add_review(review)
        return review
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            return []
        return place.reviews
    
    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        review.update(review_data)
        return review
    
    def delete_review(self, review_id):
        """Delete a review"""
        return self.review_repo.delete(review_id)
    
    # ========== Amenity Methods (if needed) ==========
    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

# Create a single instance
facade = HBnBFacade()
