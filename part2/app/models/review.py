"""
Review model
"""
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review class for managing review data"""
    
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            **super().to_dict(),
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        }
