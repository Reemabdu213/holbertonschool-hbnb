#!/usr/bin/env python3
"""
Review Model
"""
from app.models.base_model import BaseModel
from app import db 

class Review(BaseModel):
    """Review class"""
    
    """ def __init__(self, text, rating, place, user):
        #Initialize Review
        super().__init__()
        
        self.text = self._validate_text(text)
       self.rating = self._validate_rating(rating)
        self.place = place
        self.user = user
    """
         
    # Task 7
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # ✅ Foreign Keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # ✅ Relationships
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')
    def _validate_text(self, text):
        """Validate review text"""
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        
        text = text.strip()
        if len(text) == 0:
            raise ValueError("Review text cannot be empty")
        
        return text
    
    def _validate_rating(self, rating):
        """Validate rating"""
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be an integer")
        
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        return rating
    
    def update(self, data):
        """Update review data"""
        if 'text' in data:
            self.text = self._validate_text(data['text'])
        
        if 'rating' in data:
            self.rating = self._validate_rating(data['rating'])
        
        self.save()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id
        })
        return data
    
    def __repr__(self):
        """String representation"""
        return f"<Review {self.id}: {self.rating}/5 stars>"
