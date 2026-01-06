"""
Amenity model
"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class for managing amenity data"""
    
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def to_dict(self):
        """Convert amenity to dictionary"""
        return {
            **super().to_dict(),
            'name': self.name
        }
