#!/usr/bin/env python3
"""
Place Model
"""
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place class"""
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize Place"""
        super().__init__()
        
        self.title = self._validate_title(title)
        self.description = description if description else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner
        
        self.reviews = []
        self.amenities = []
    
    def _validate_title(self, title):
        """Validate title"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        
        title = title.strip()
        if len(title) == 0:
            raise ValueError("Title cannot be empty")
        
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        
        return title
    
    def _validate_price(self, price):
        """Validate price"""
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        return price
    
    def _validate_latitude(self, latitude):
        """Validate latitude"""
        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        return latitude
    
    def _validate_longitude(self, longitude):
        """Validate longitude"""
        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        return longitude
    
    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
    
    def update(self, data):
        """Update place data"""
        if 'title' in data:
            self.title = self._validate_title(data['title'])
        
        if 'description' in data:
            self.description = data['description']
        
        if 'price' in data:
            self.price = self._validate_price(data['price'])
        
        if 'latitude' in data:
            self.latitude = self._validate_latitude(data['latitude'])
        
        if 'longitude' in data:
            self.longitude = self._validate_longitude(data['longitude'])
        
        self.save()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'amenities': [amenity.id for amenity in self.amenities]
        })
        return data
    
    def __repr__(self):
        """String representation"""
        return f"<Place {self.id}: {self.title}>"
