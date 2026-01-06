"""
Place model
"""
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place class for managing place data"""
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List of review IDs
        self.amenities = []  # List of amenity IDs
    
    def add_review(self, review_id):
        """Add a review to the place"""
        self.reviews.append(review_id)
    
    def add_amenity(self, amenity_id):
        """Add an amenity to the place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
    
    def to_dict(self):
        """Convert place to dictionary"""
        return {
            **super().to_dict(),
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }
