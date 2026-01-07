#!/usr/bin/env python3
"""
User Model
"""
from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """User class"""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize User"""
        super().__init__()
        
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        
        self.places = []
        self.reviews = []
    
    def _validate_name(self, name, field_name):
        """Validate name"""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        
        name = name.strip()
        if len(name) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        
        if len(name) > 50:
            raise ValueError(f"{field_name} must be 50 characters or less")
        
        return name
    
    def _validate_email(self, email):
        """Validate email"""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email = email.strip().lower()
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        
        return email
    
    def update(self, data):
        """Update user data"""
        if 'first_name' in data:
            self.first_name = self._validate_name(data['first_name'], "First name")
        
        if 'last_name' in data:
            self.last_name = self._validate_name(data['last_name'], "Last name")
        
        if 'email' in data:
            self.email = self._validate_email(data['email'])
        
        self.save()
    
    def add_place(self, place):
        """Add a place to user"""
        if place not in self.places:
            self.places.append(place)
    
    def add_review(self, review):
        """Add a review to user"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data
    
    def __repr__(self):
        """String representation"""
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
