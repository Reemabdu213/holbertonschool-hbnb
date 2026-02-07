#!/usr/bin/env python3
"""
BaseModel
"""
from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """ The main class for the models"""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ لا يوجد __init__ - SQLAlchemy يتولاها تلقائياً
    
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
        db.session.commit()
    
    def update(self, data):
        """
        Update object attributes from a dictionary
        Args:
            data (dict): Dictionary containing updated values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
    
    def to_dict(self):
        """Convert object attributes to a dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
