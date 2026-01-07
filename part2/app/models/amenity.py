#!/usr/bin/env python3
"""
Amenity Model
"""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class"""
    
    def __init__(self, name):
        """Initialize Amenity"""
        super().__init__()
        self.name = self._validate_name(name)
    
    def _validate_name(self, name):
        """Validate amenity name"""
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        
        name = name.strip()
        if len(name) == 0:
            raise ValueError("Amenity name cannot be empty")
        
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        
        return name
    
    def update(self, data):
        """Update amenity data"""
        if 'name' in data:
            self.name = self._validate_name(data['name'])
        
        self.save()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data['name'] = self.name
        return data
    
    def __repr__(self):
        """String representation"""
        return f"<Amenity {self.id}: {self.name}>"
